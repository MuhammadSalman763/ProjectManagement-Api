from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskUpdateView,
)


urlpatterns = [
    # User registration
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # User login
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    # User logout
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Project creation
    path(
        "projects/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),

    # Project list
    path(
        "projects/list/",
        ProjectListView.as_view(),
        name="project-list",
    ),

    # Project detail
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),

    # Project update
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),

    # Project delete
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),


    # Ticket 9: Task creation

     path(
    "tasks/",
    TaskCreateView.as_view(),
    name="task-create",
     ),


      # Ticket 10: List tasks
    path(
    "tasks/list/",
    TaskListView.as_view(),
    name="task-list",
       ),



    # Ticket 11: Task detail
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),

    # Ticket 12: Task update
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
]