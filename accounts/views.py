from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Task, Document,Comment

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProjectSerializer,
    TaskSerializer,
    TaskAssignSerializer,
    DocumentSerializer,
    CommentSerializer,
)


# Ticket 1: User Registration API
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully.",
                "user": RegisterSerializer(
                    user,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# Ticket 2: User Login API
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(
            {
                "message": "Login successful.",
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "User logged out successfully.",
            },
            status=status.HTTP_200_OK,
        )


# Ticket 4: Project Creation API
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


# Ticket 5: Project List API
class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


# Ticket 6: Project Detail API
class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


# Ticket 7: Project Update API
class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


# Ticket 8: Project Delete API
class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()

        return Response(
            {
                "message": "Project deleted successfully."
            },
            status=status.HTTP_200_OK,
        )


# Ticket 9: Create Task API
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# Ticket 10: List Tasks API
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# Ticket 11: Task Detail API
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# Ticket 12: Update Task API
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# Ticket 13: Delete Task API
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()

        return Response(
            {
                "message": "Task deleted successfully."
            },
            status=status.HTTP_200_OK,
        )


# Ticket 14: Task Assignment API
class TaskAssignView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskAssignSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        task = self.get_object()

        serializer = self.get_serializer(
            data=request.data,
            context={"task": task},
        )

        serializer.is_valid(raise_exception=True)

        task = serializer.save()

        return Response(
            {
                "message": "Task assigned successfully.",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "assignee": {
                        "id": task.assignee.id,
                        "username": task.assignee.username,
                    }
                    if task.assignee
                    else None,
                },
            },
            status=status.HTTP_200_OK,
        )


# Ticket 15: Upload Document API
class DocumentUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DocumentSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        document = serializer.save()

        return Response(
            {
                "message": "Document uploaded successfully.",
                "document": DocumentSerializer(
                    document,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# Ticket 16: List Documents API
class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get("project")

        if project_id:
            return Document.objects.filter(
                project_id=project_id,
                project__team_members=self.request.user,
            )

        return Document.objects.filter(
            project__team_members=self.request.user
        ).distinct()


# Ticket 17: Document Detail API
class DocumentDetailView(generics.RetrieveAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            project__team_members=self.request.user
        ).distinct()   

# Ticket 18: Update Document API
class DocumentUpdateView(generics.UpdateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Document.objects.filter(
            project__team_members=self.request.user
        ).distinct()

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)

        document = serializer.save()

        return Response(
            {
                "message": "Document updated successfully.",
                "document": DocumentSerializer(
                    document,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )    


  # Ticket 19: Delete Document API
class DocumentDeleteView(generics.DestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            project__team_members=self.request.user
        ).distinct()

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        document.delete()

        return Response(
            {
                "message": "Document deleted successfully."
            },
            status=status.HTTP_200_OK
        )  

# Ticket 20: Create Comment API
class CommentCreateView(generics.CreateAPIView):

    queryset = Comment.objects.all()

    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)    