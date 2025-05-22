from django.urls import path
from . import views

urlpatterns = [
    path('facilities/', views.facilities_view, name='facilities'),
    path('facilities/create/', views.facility_create_view, name='facility_create'),
    path('facilities/<int:pk>/edit/', views.facility_edit_view, name='facility_edit'),
    path('devices/', views.devices_view, name='devices'),
    path('devices/create/', views.device_create_view, name='device_create'),
    path('devices/<int:pk>/edit/', views.device_edit_view, name='device_edit'),
    path('devices/<int:pk>/view/', views.device_detail_view, name='device_view'),
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),
    path('passes/', views.passes_view, name='passes'),
    path('passes/create/', views.pass_create_view, name='pass_create'),
    path('passes/<int:pk>/delete/', views.pass_delete_view, name='pass_delete'),
    path('passes/<int:pk>/qr/', views.pass_qr_view, name='pass_qr'),
    path('logs/', views.logs_view, name='logs'),
]