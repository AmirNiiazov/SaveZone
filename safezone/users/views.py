from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register_view(request):
    return render(request, 'users/register.html')


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
@user_passes_test(lambda u: u.role == 'superadmin')
def invites_view(request):
    return render(request, 'users/invites.html')
