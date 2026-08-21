from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Project,Task
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProjectSerializer,
    TaskAssignSerializer,
    TaskSerializer,
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


# Project List API
class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


# Project Detail API
class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


# Project Update API
class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


# Project Delete API
class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()

        return Response(
            {
                "message": "Project deleted successfully."
            },
            status=status.HTTP_200_OK
        )


# Ticket 9: Create Task API

class TaskCreateView(generics.CreateAPIView):

    queryset = Task.objects.all()

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save()    


# Ticket 10: List Tasks API
# Returns all tasks for authenticated users.

class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# Ticket 11: Task Detail API
# Returns details of a specific task.

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]



# Ticket 12: Update Task API
# Allows authenticated users to update an existing task.

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# Ticket 13: Delete Task API
# Allows authenticated users to delete an existing task.

class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()

        return Response(
            {
                "message": "Task deleted successfully."
            },
            status=status.HTTP_200_OK
        )    

class TaskAssignView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskAssignSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        task = self.get_object()

        serializer = self.get_serializer(
            data=request.data,
            context={"task": task}
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
                    } if task.assignee else None,
                },
            },
            status=status.HTTP_200_OK
        )