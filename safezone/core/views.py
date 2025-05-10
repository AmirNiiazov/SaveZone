from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(lambda u: u.role in ['superadmin', 'technician'])
def facilities_view(request):
    return render(request, 'core/facilities.html')


@login_required
@user_passes_test(lambda u: u.role in ['superadmin', 'technician', 'admin'])
def devices_view(request):
    return render(request, 'core/devices.html')


@login_required
def passes_view(request):
    return render(request, 'core/passes.html')


@login_required
def logs_view(request):
    return render(request, 'core/logs.html')


@login_required
@user_passes_test(lambda u: u.role in ['superadmin', 'technician', 'admin'])
def guards_view(request):
    return render(request, 'core/guards.html')


