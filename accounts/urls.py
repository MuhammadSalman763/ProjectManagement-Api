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
    DocumentDeleteView,
    CommentCreateView,
    CommentListView,
    CommentUpdateView,
    CommentDeleteView,
    CommentDetailView,
    ProjectCommentsView,
    TimelineEventListView,
    NotificationListView,
    NotificationMarkReadView,
)


urlpatterns = [

    # Ticket 1: User Registration
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # Ticket 2: User Login
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    # Ticket 3: User Logout
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Ticket 4: Project Creation
    path(
        "projects/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),

    # Ticket 5: Project List
    path(
        "projects/list/",
        ProjectListView.as_view(),
        name="project-list",
    ),

    # Ticket 6: Project Detail
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),

    # Ticket 7: Project Update
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),

    # Ticket 8: Project Delete
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),

    # Ticket 9: Task Creation
    path(
        "tasks/",
        TaskCreateView.as_view(),
        name="task-create",
    ),

    # Ticket 10: Task List
    path(
        "tasks/list/",
        TaskListView.as_view(),
        name="task-list",
    ),

    # Ticket 11: Task Detail
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),

    # Ticket 12: Task Update
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),

    # Ticket 13: Task Delete
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),

    # Ticket 14: Task Assignment
    path(
        "tasks/<int:pk>/assign/",
        TaskAssignView.as_view(),
        name="task-assign",
    ),

    # Ticket 15: Upload Document
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

    # Ticket 19: Delete Document
    path(
        "documents/<int:pk>/delete/",
        DocumentDeleteView.as_view(),
        name="document-delete",
    ),

    # Ticket 20: Create Comment
    path(
        "comments/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),

    # Ticket 21: List Comments
    path(
        "comments/list/",
        CommentListView.as_view(),
        name="comment-list",
    ),

    # Ticket 22: Update Comment
    path(
        "comments/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),

    # Ticket 23: Delete Comment
    path(
        "comments/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),

    # Ticket 24: Comment Detail
    path(
        "comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),

    # Ticket 25: Project Comments
    path(
        "projects/<int:project_id>/comments/",
        ProjectCommentsView.as_view(),
        name="project-comments",
    ),

    # Ticket 26: Timeline Events
    path(
        "timeline/",
        TimelineEventListView.as_view(),
        name="timeline-list",
    ),

    # Ticket 27: Notifications
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="notification-list",
    ),

    # Ticket 28: Mark Notification as Read
    path(
        "notifications/<int:pk>/mark_read/",
        NotificationMarkReadView.as_view(),
        name="notification-mark-read",
    ),
]