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
    TaskDeleteView,
    TaskAssignView,
    DocumentUploadAPIView,
    DocumentListView,
    DocumentDetailView,
    DocumentUpdateView,
)


urlpatterns = [

    # Ticket 1: User registration
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # Ticket 2: User login
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    # Ticket 3: User logout
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Ticket 4: Project creation
    path(
        "projects/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),

    # Ticket 5: Project list
    path(
        "projects/list/",
        ProjectListView.as_view(),
        name="project-list",
    ),

    # Ticket 6: Project detail
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),

    # Ticket 7: Project update
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),

    # Ticket 8: Project delete
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

    # Ticket 13: Task delete
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),

    # Ticket 14: Task assignment
    path(
        "tasks/<int:pk>/assign/",
        TaskAssignView.as_view(),
        name="task-assign",
    ),

    # Ticket 15: Upload document
    path(
        "documents/",
        DocumentUploadAPIView.as_view(),
        name="document-upload",
    ),

    # Ticket 16: List Documents
     path(
    "documents/list/",
    DocumentListView.as_view(),
    name="document-list",
      ),
    # Ticket 17: Document Detail
    path(
        "documents/<int:pk>/",
        DocumentDetailView.as_view(),
        name="document-detail",
    ),
    # Ticket 18: Update Document
    path(
        "documents/<int:pk>/update/",
        DocumentUpdateView.as_view(),
        name="document-update",
    ),
]