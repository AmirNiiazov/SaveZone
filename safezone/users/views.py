from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator
from users.models import User
from core.models import Facilities, Devices, AccessPasses, AccessLogs
from .models import Invite
from .forms import InviteForm, RegistrationForm
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register_view(request):
    token = request.GET.get('token')
    invite = get_object_or_404(Invite, token=token, used_at__isnull=True)

    if request.method == 'POST':
        temp_user = User(username=invite.email)  # временный пользователь для SetPasswordForm
        form = RegistrationForm(user=temp_user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = invite.email
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = invite.email
            user.role = invite.role
            user.facility = invite.facility
            user.save()
            invite.used_at = timezone.now()
            invite.save()
            login(request, user)
            return redirect('dashboard')
    else:
        temp_user = User(username=invite.email)
        form = RegistrationForm(user=temp_user)

    return render(request, 'users/register.html', {'form': form, 'invite': invite})


@login_required
def dashboard_view(request):
    context = {}

    if request.user.role == 'superadmin':
        context.update({
            'admin_count': User.objects.filter(role='admin').count(),
            'technician_count': User.objects.filter(role='technician').count(),
            'facility_count': Facilities.objects.count(),
            'device_count': Devices.objects.count(),
            'latest_facilities': Facilities.objects.order_by('-created_at')[:5],
            'latest_devices': Devices.objects.order_by('-created_at')[:5],
        })

    elif request.user.role == 'admin' and request.user.facility:
        facility = request.user.facility
        devices = Devices.objects.filter(facility=facility)
        passes = AccessPasses.objects.filter(facility=facility)
        logs = AccessLogs.objects.filter(device__facility=facility)
        today = now().date()

        context.update({
            'device_count': devices.count(),
            'pass_count': passes.count(),
            'log_count': logs.count(),
            'log_today_count': logs.filter(timestamp__date=today).count(),
            'latest_passes': passes.order_by('-created_at')[:5],
            'latest_logs': logs.order_by('-timestamp')[:5],
        })

    elif request.user.role == 'technician':
        logs_last_week = AccessLogs.objects.filter(timestamp__gte=now() - timedelta(days=7))
        context.update({
            'facility_count': Facilities.objects.count(),
            'device_count': Devices.objects.count(),
            'pass_count': AccessPasses.objects.count(),
            'log_week_count': logs_last_week.count(),
            'latest_devices': Devices.objects.order_by('-created_at')[:5],
            'latest_logs': AccessLogs.objects.order_by('-timestamp')[:5],
        })

    return render(request, 'users/dashboard.html', context)


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
@user_passes_test(lambda u: u.role == 'superadmin')
def invites_view(request):
    query = request.GET.get('q', '').strip()
    invites = Invite.objects.select_related('facility')

    if query:
        invites = invites.filter(
            Q(email__icontains=query) |
            Q(facility__title__icontains=query)
        )

    invites = invites.order_by('-created_at')

    paginator = Paginator(invites, 25)  # по 25 приглашений на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/invites.html', {
        'page_obj': page_obj,
        'invites': page_obj,  # используем в шаблоне
        'query': query,
    })


@login_required
@user_passes_test(lambda u: u.role == 'superadmin')
def invite_create_view(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invites')
    else:
        form = InviteForm()

    return render(request, 'users/partials/invite_create.html', {'form': form})