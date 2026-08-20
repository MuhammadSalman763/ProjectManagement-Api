from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProjectCreateView,
)

urlpatterns = [
    # User registration
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    # User login
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),

    # User logout
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    # Project creation
    path(
        'projects/',
        ProjectCreateView.as_view(),
        name='project-create'
    ),
]