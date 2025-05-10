from django.urls import path
from . import views

urlpatterns = [
    path('facilities/', views.facilities_view, name='facilities'),
    path('devices/', views.devices_view, name='devices'),
    path('passes/', views.passes_view, name='passes'),
    path('logs/', views.logs_view, name='logs'),
    path('guards/', views.guards_view, name='guards'),
]