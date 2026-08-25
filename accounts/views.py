from django.db.models import Q

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Project,
    Task,
    Document,
    Comment,
    TimelineEvent,
    Notification,
)

from .permissions import (
    IsCommentAuthor,
    IsProjectTeamMember,
)

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProjectSerializer,
    TaskSerializer,
    TaskAssignSerializer,
    DocumentSerializer,
    CommentSerializer,
    TimelineEventSerializer,
    NotificationSerializer,
)


# Ticket 1: User Registration API
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "message": (
                    "User registered successfully."
                ),
                "user": RegisterSerializer(
                    user,
                    context={
                        "request": request
                    },
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# Ticket 2: User Login API
class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data[
            "user"
        ]

        return Response(
            {
                "message": "Login successful.",
                "access": serializer.validated_data[
                    "access"
                ],
                "refresh": serializer.validated_data[
                    "refresh"
                ],
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.profile.role,
                },
            },
            status=status.HTTP_200_OK,
        )


# Ticket 3: User Logout API
class LogoutView(generics.GenericAPIView):

    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": (
                    "User logged out successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


# Ticket 4: Project Creation API
class ProjectCreateView(generics.CreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        project = serializer.save()

        project.team_members.add(
            self.request.user
        )

        TimelineEvent.objects.create(
            project=project,
            user=self.request.user,
            event_type="project_created",
            description=(
                f"Project '{project.title}' "
                "was created."
            ),
        )


# Ticket 5: Project List API
class ProjectListView(generics.ListAPIView):

    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Project.objects.filter(
            team_members=self.request.user
        ).distinct()


# Ticket 6: Project Detail API
class ProjectDetailView(generics.RetrieveAPIView):

    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Project.objects.filter(
            team_members=self.request.user
        ).distinct()


# Ticket 7: Project Update API
class ProjectUpdateView(generics.UpdateAPIView):

    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Project.objects.filter(
            team_members=self.request.user
        ).distinct()


# Ticket 8: Project Delete API
class ProjectDeleteView(generics.DestroyAPIView):

    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Project.objects.filter(
            team_members=self.request.user
        ).distinct()

    def destroy(self, request, *args, **kwargs):

        project = self.get_object()

        project.delete()

        return Response(
            {
                "message": (
                    "Project deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


# Ticket 9: Create Task API
class TaskCreateView(generics.CreateAPIView):

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        project = serializer.validated_data.get(
            "project"
        )

        if not project.team_members.filter(
            id=self.request.user.id
        ).exists():

            raise PermissionDenied(
                "You must be a member of the project team."
            )

        serializer.save()


# Ticket 10: List Tasks API
class TaskListView(generics.ListAPIView):

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Task.objects.filter(
            project__team_members=self.request.user
        ).distinct()


# Ticket 11: Task Detail API
class TaskDetailView(generics.RetrieveAPIView):

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Task.objects.filter(
            project__team_members=self.request.user
        ).distinct()


# Ticket 12: Update Task API
class TaskUpdateView(generics.UpdateAPIView):

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Task.objects.filter(
            project__team_members=self.request.user
        ).distinct()


# Ticket 13: Delete Task API
class TaskDeleteView(generics.DestroyAPIView):

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Task.objects.filter(
            project__team_members=self.request.user
        ).distinct()

    def destroy(self, request, *args, **kwargs):

        task = self.get_object()

        task.delete()

        return Response(
            {
                "message": (
                    "Task deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


# Ticket 14: Assign Task API
class TaskAssignView(generics.GenericAPIView):

    serializer_class = TaskAssignSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Task.objects.filter(
            project__team_members=self.request.user
        ).distinct()

    def post(self, request, *args, **kwargs):

        task = self.get_object()

        serializer = self.get_serializer(
            data=request.data,
            context={
                "task": task,
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        task = serializer.save()

        if task.assignee is None:

            return Response(
                {
                    "error": (
                        "Task could not be assigned."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        Notification.objects.create(
            user=task.assignee,
            message=(
                f"You have been assigned task "
                f"'{task.title}'."
            ),
        )

        TimelineEvent.objects.create(
            project=task.project,
            user=request.user,
            event_type="task_assigned",
            description=(
                f"Task '{task.title}' was assigned "
                f"to {task.assignee.username}."
            ),
        )

        return Response(
            {
                "message": (
                    "Task assigned successfully."
                ),
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "assignee": {
                        "id": task.assignee.id,
                        "username": (
                            task.assignee.username
                        ),
                    },
                },
            },
            status=status.HTTP_200_OK,
        )


# Ticket 15: Upload Document API
class DocumentUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request):

        serializer = DocumentSerializer(
            data=request.data,
            context={
                "request": request
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        document = serializer.save()

        return Response(
            {
                "message": (
                    "Document uploaded successfully."
                ),
                "document": DocumentSerializer(
                    document,
                    context={
                        "request": request
                    },
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# Ticket 16: List Documents API
class DocumentListView(generics.ListAPIView):

    serializer_class = DocumentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        project_id = (
            self.request.query_params.get(
                "project"
            )
        )

        if project_id:

            return Document.objects.filter(
                project_id=project_id,
                project__team_members=(
                    self.request.user
                ),
            ).distinct()

        return Document.objects.filter(
            project__team_members=(
                self.request.user
            )
        ).distinct()


# Ticket 17: Document Detail API
class DocumentDetailView(generics.RetrieveAPIView):

    serializer_class = DocumentSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Document.objects.filter(
            project__team_members=(
                self.request.user
            )
        ).distinct()


# Ticket 18: Update Document API
class DocumentUpdateView(generics.UpdateAPIView):

    serializer_class = DocumentSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):

        return Document.objects.filter(
            project__team_members=(
                self.request.user
            )
        ).distinct()

    def update(self, request, *args, **kwargs):

        partial = (
            request.method == "PATCH"
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        document = serializer.save()

        return Response(
            {
                "message": (
                    "Document updated successfully."
                ),
                "document": DocumentSerializer(
                    document,
                    context={
                        "request": request
                    },
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# Ticket 19: Delete Document API
class DocumentDeleteView(generics.DestroyAPIView):

    serializer_class = DocumentSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectTeamMember,
    ]

    def get_queryset(self):

        return Document.objects.filter(
            project__team_members=(
                self.request.user
            )
        ).distinct()

    def destroy(self, request, *args, **kwargs):

        document = self.get_object()

        document.delete()

        return Response(
            {
                "message": (
                    "Document deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


# Ticket 20: Create Comment API
class CommentCreateView(generics.CreateAPIView):

    queryset = Comment.objects.all()

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )


# Ticket 21: List Comments API
class CommentListView(generics.ListAPIView):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Comment.objects.filter(
            Q(
                task__project__team_members=user
            )
            |
            Q(
                project__team_members=user
            )
        ).distinct()

        task_id = (
            self.request.query_params.get(
                "task"
            )
        )

        project_id = (
            self.request.query_params.get(
                "project"
            )
        )

        if task_id:

            queryset = queryset.filter(
                task_id=task_id
            )

        if project_id:

            queryset = queryset.filter(
                project_id=project_id
            )

        return queryset


# Ticket 22: Update Comment API
class CommentUpdateView(generics.UpdateAPIView):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated,
        IsCommentAuthor,
    ]

    def get_queryset(self):

        return Comment.objects.filter(
            author=self.request.user
        )


# Ticket 23: Delete Comment API
class CommentDeleteView(generics.DestroyAPIView):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated,
        IsCommentAuthor,
    ]

    def get_queryset(self):

        return Comment.objects.filter(
            author=self.request.user
        )

    def destroy(self, request, *args, **kwargs):

        comment = self.get_object()

        comment.delete()

        return Response(
            {
                "message": (
                    "Comment deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


# Ticket 24: Comment Detail API
class CommentDetailView(generics.RetrieveAPIView):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        return Comment.objects.filter(
            Q(
                task__project__team_members=user
            )
            |
            Q(
                project__team_members=user
            )
        ).distinct()


# Ticket 25: Project Comments API
class ProjectCommentsView(generics.ListAPIView):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        project_id = self.kwargs[
            "project_id"
        ]

        user = self.request.user

        return Comment.objects.filter(
            project_id=project_id,
            project__team_members=user,
        ).distinct()


# Ticket 26: Timeline Events API
class TimelineEventListView(generics.ListAPIView):

    serializer_class = TimelineEventSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        user = self.request.user

        return (
            TimelineEvent.objects
            .filter(
                project__team_members=user
            )
            .select_related(
                "project",
                "user",
            )
            .order_by("-created_at")
        )


# Ticket 27: Notifications API
class NotificationListView(generics.ListAPIView):

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


# Ticket 28: Mark Notification as Read API
class NotificationMarkReadView(
    generics.UpdateAPIView
):

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        )

    def update(self, request, *args, **kwargs):

        notification = self.get_object()

        notification.is_read = True

        notification.save(
            update_fields=[
                "is_read"
            ]
        )

        return Response(
            {
                "message": (
                    "Notification marked as read."
                ),
                "notification": (
                    NotificationSerializer(
                        notification,
                        context={
                            "request": request
                        },
                    ).data
                ),
            },
            status=status.HTTP_200_OK,
        )