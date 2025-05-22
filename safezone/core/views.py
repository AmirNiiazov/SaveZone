from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Facilities, Devices, AccessLogs, AccessPasses
from .forms import FacilityForm, DeviceForm, AccessPassForm
from .service import OrangePiClient


@login_required
@user_passes_test(lambda u: u.role in ['superadmin', 'technician'])
def facilities_view(request):
    query = request.GET.get('q', '').strip()
    facilities = Facilities.objects.filter(title__icontains=query) if query else Facilities.objects.all()

    return render(request, 'core/facilities.html', {
        'facilities': facilities,
        'query': query,
    })


@login_required
@user_passes_test(lambda u: u.role == 'superadmin')
def facility_create_view(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facilities')
    else:
        form = FacilityForm()

    return render(request, 'core/partials/facility_create.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.role == 'superadmin')
def facility_edit_view(request, pk):
    facility = get_object_or_404(Facilities, pk=pk)

    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            return redirect('facilities')
    else:
        form = FacilityForm(instance=facility)

    return render(request, 'core/partials/facility_edit.html', {
        'form': form,
        'facility': facility,
    })


@login_required
def devices_view(request):
    query = request.GET.get('q', '').strip()

    if request.user.role == 'admin':
        devices = Devices.objects.filter(facility=request.user.facility)
    else:
        devices = Devices.objects.select_related('facility').all()

    if query:
        devices = devices.filter(
            Q(title__icontains=query) |
            Q(facility__title__icontains=query)
        )

    return render(request, 'core/devices.html', {
        'devices': devices,
        'query': query,
    })


@login_required
@user_passes_test(lambda u: u.role in ['superadmin', 'technician'])
def device_create_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devices')
    else:
        form = DeviceForm()
    return render(request, 'core/partials/device_create.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.role in ['superadmin', 'technician'])
def device_edit_view(request, pk):
    device = get_object_or_404(Devices, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('devices')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'core/partials/device_edit.html', {'form': form, 'device': device})


@login_required
def device_detail_view(request, pk):
    device = get_object_or_404(Devices, pk=pk)
    return render(request, 'core/partials/device_view.html', {'device': device})


@login_required
@user_passes_test(lambda u: u.role in ['superadmin', 'technician'])
def device_delete(request, pk):
    device = get_object_or_404(Devices, pk=pk)

    if request.method == 'POST':
        device.delete()
        return redirect('devices')

    return render(request, 'core/device_confirm_delete.html', {'device': device})


@login_required
def passes_view(request):
    user = request.user
    query = request.GET.get('q', '').strip()

    # 🔎 Базовый queryset
    if user.role == 'admin':
        passes = AccessPasses.objects.filter(facility=user.facility)
    else:
        passes = AccessPasses.objects.all()

    # 🔍 Поиск по ролям
    if query:
        if user.role == 'admin':
            passes = passes.filter(
                Q(full_name__icontains=query) |
                Q(device__title__icontains=query)
            )
        else:
            passes = passes.filter(
                Q(full_name__icontains=query) |
                Q(facility__title__icontains=query) |
                Q(device__title__icontains=query)
            )

    passes = passes.select_related('device', 'device__facility').order_by('-created_at')

    paginator = Paginator(passes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/passes.html', {
        'page_obj': page_obj,
        'query': query,
    })


@login_required
def pass_create_view(request):
    if request.method == 'POST':
        form = AccessPassForm(request.POST, user=request.user)
        if form.is_valid():
            access_pass = form.save(commit=False)
            access_pass.facility = request.user.facility
            access_pass.save()
            if access_pass.device:
                res = OrangePiClient(device_id=access_pass.device.id).send_pass(access_pass.pk)
            else:
                res = OrangePiClient(facility_id=access_pass.facility_id).send_pass(access_pass.pk)
            if not res:
                messages.error(request, "Ошибка при отправке пропуска на турникет.")
                access_pass.delete()
            return redirect('passes')
    else:
        form = AccessPassForm(user=request.user)

    return render(request, 'core/partials/pass_form.html', {'form': form, 'title': 'Создать пропуск'})


@login_required
def pass_delete_view(request, pk):
    access_pass = get_object_or_404(AccessPasses, pk=pk, facility=request.user.facility)

    if request.method == 'POST':
        if access_pass.device:
            res = OrangePiClient(device_id=access_pass.device.id).delete_pass(access_pass.pk)
        else:
            res = OrangePiClient(facility_id=access_pass.facility_id).delete_pass(access_pass.pk)
        if not res:
            messages.error(request, "Ошибка при удалении пропуска с турникета.")
        else:
            access_pass.delete()
        return redirect('passes')

    return render(request, 'core/partials/pass_confirm_delete.html', {'pass_obj': access_pass})


@login_required
def pass_qr_view(request, pk):
    access_pass = get_object_or_404(AccessPasses, pk=pk, facility=request.user.facility)
    return render(request, 'core/partials/pass_qr_view.html', {'pass_obj': access_pass})


@login_required
def logs_view(request):
    user = request.user
    query = request.GET.get('q', '').strip()

    logs = AccessLogs.objects.select_related('device', 'access_pass', 'device__facility')

    if user.role == 'admin':
        logs = logs.filter(device__facility=user.facility)

    logs = logs.order_by('-timestamp')
    if query:
        if user.role == 'admin':
            logs = logs.filter(
                Q(access_pass__full_name__icontains=query) |
                Q(device__title__icontains=query)
            )
        else:
            logs = logs.filter(
                Q(access_pass__full_name__icontains=query) |
                Q(device__facility__title__icontains=query) |
                Q(device__title__icontains=query)
            )

    paginator = Paginator(logs, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/logs.html', {
        'page_obj': page_obj,
        'query': query,
    })



