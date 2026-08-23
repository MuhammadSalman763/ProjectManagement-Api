from django.contrib import admin

from .models import (
    Profile,
    Project,
    Task,
    Document,
    Comment,
    TimelineEvent,
    Notification,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "contact_number",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "user__username",
        "user__email",
        "contact_number",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start_date",
        "end_date",
    )

    list_filter = (
        "start_date",
        "end_date",
    )

    search_fields = (
        "title",
        "description",
    )

    filter_horizontal = (
        "team_members",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "project",
        "assignee",
    )

    list_filter = (
        "status",
        "project",
    )

    search_fields = (
        "title",
        "description",
        "assignee__username",
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "version",
    )

    list_filter = (
        "project",
        "version",
    )

    search_fields = (
        "name",
        "description",
        "project__title",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "author",
        "task",
        "project",
        "created_at",
    )

    list_filter = (
        "created_at",
        "project",
        "task",
    )

    search_fields = (
        "text",
        "author__username",
    )


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = (
        "event_type",
        "project",
        "user",
        "created_at",
    )

    list_filter = (
        "event_type",
        "project",
        "created_at",
    )

    search_fields = (
        "event_type",
        "description",
        "user__username",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "message",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "message",
    )