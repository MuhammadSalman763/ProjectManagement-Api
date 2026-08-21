from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("qa", "QA"),
        ("developer", "Developer"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="developer"
    )

    contact_number = models.BigIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username


class Project(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField()

    team_members = models.ManyToManyField(
        User,
        related_name="projects",
        blank=True
    )

    def __str__(self):
        return self.title


class Task(models.Model):

    STATUS_CHOICES = [
        ("open", "Open"),
        ("review", "Review"),
        ("working", "Working"),
        ("awaiting_release", "Awaiting Release"),
        ("waiting_qa", "Waiting QA"),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="open"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    def __str__(self):
        return self.title