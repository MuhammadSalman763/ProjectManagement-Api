from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Profile,
    Project,
    Task,
    Document,
    Comment,
    TimelineEvent,
    Notification,
)


# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        default="developer",
    )

    contact_number = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    profile_picture = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "contact_number",
            "profile_picture",
        ]
        read_only_fields = ["id"]

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError(
                "Username should only contain alphanumeric characters."
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def create(self, validated_data):
        role = validated_data.pop("role", "developer")
        contact_number = validated_data.pop("contact_number", None)
        profile_picture = validated_data.pop("profile_picture", None)
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        Profile.objects.create(
            user=user,
            role=role,
            contact_number=contact_number,
            profile_picture=profile_picture,
        )

        return user

    def to_representation(self, instance):
        profile = instance.profile
        request = self.context.get("request")

        if profile.profile_picture:
            picture_added = True

            if request:
                picture_url = request.build_absolute_uri(
                    profile.profile_picture.url
                )
            else:
                picture_url = profile.profile_picture.url
        else:
            picture_added = False
            picture_url = None

        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "role": profile.role,
            "contact_number": profile.contact_number,
            "profile_picture_added": picture_added,
            "profile_picture": picture_url,
        }


# User Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is disabled."
            )

        refresh = RefreshToken.for_user(user)

        attrs["user"] = user
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)

        return attrs


# User Logout Serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        required=True,
    )

    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except Exception:
            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            )

        return value

    def save(self, **kwargs):
        refresh_token = self.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            )

        return {
            "message": "User logged out successfully.",
        }


# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "team_members",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if self.instance:
            if start_date is None:
                start_date = self.instance.start_date

            if end_date is None:
                end_date = self.instance.end_date

        if (
            start_date is not None
            and end_date is not None
        ):
            if end_date < start_date:
                raise serializers.ValidationError(
                    {
                        "end_date": (
                            "End date cannot be before start date."
                        )
                    }
                )

        return attrs


# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "project",
            "assignee",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        project = attrs.get("project")
        assignee = attrs.get("assignee")

        if assignee and project:
            if not project.team_members.filter(
                id=assignee.id
            ).exists():
                raise serializers.ValidationError(
                    {
                        "assignee": (
                            "Assignee must be a member "
                            "of the project team."
                        )
                    }
                )

        return attrs


# Task Assignment Serializer
class TaskAssignSerializer(serializers.Serializer):
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    def validate_assignee(self, value):
        task = self.context["task"]

        if not task.project.team_members.filter(
            id=value.id
        ).exists():
            raise serializers.ValidationError(
                "Assignee must be a member of the project team."
            )

        return value

    def save(self, **kwargs):
        task = self.context["task"]
        assignee = self.validated_data["assignee"]

        task.assignee = assignee
        task.save(
            update_fields=["assignee"]
        )

        return task


# Document Serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "description",
            "file",
            "version",
            "project",
        ]
        read_only_fields = ["id"]

    def validate_project(self, value):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            if not value.team_members.filter(
                id=request.user.id
            ).exists():
                raise serializers.ValidationError(
                    "You must be a member of the project "
                    "to upload a document."
                )

        return value


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "author",
            "created_at",
            "task",
            "project",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
        ]

    def validate(self, attrs):
        task = attrs.get("task")
        project = attrs.get("project")

        if self.instance:
            if task is None:
                task = self.instance.task

            if project is None:
                project = self.instance.project

        if task is None and project is None:
            raise serializers.ValidationError(
                "Comment must belong to a task or a project."
            )

        if task is not None and project is not None:
            raise serializers.ValidationError(
                "Comment cannot belong to both a task and a project."
            )

        return attrs


# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "message",
            "is_read",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "message",
            "created_at",
        ]


# Timeline Event Serializer
class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = [
            "id",
            "project",
            "user",
            "event_type",
            "description",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]