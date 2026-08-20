from django.urls import path

from .views import (
    RegisterView,
    LoginView,
)


urlpatterns = [

    # Ticket 1: User Registration API
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    # Ticket 2: User Login API
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
]