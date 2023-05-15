from django.urls import path
from . import views

"""Url paths for User System"""

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register-other-users/', views.register_other_roles, name='register_other_users'),

    path('register/', views.register, name='register'),
    path('refresh-form/', views.refresh, name='refresh_form')


]