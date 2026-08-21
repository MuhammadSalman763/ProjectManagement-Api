from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
    ProjectUpdateView
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
    # Project list
    path(
        'projects/list/',
        ProjectListView.as_view(),
        name='project-list'
    ),
    # Project detail
    path(
        'projects/<int:pk>/',
        ProjectDetailView.as_view(),
        name='project-detail'
    ),

    # Project update
    path(
        'projects/<int:pk>/update/',
        ProjectUpdateView.as_view(),
        name='project-update'
    ),
]