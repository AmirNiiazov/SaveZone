from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('invites/', views.invites_view, name='invites'),
    path('invites/create/', views.invite_create_view, name='invite_create')
]