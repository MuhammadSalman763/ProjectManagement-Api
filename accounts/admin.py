from django.contrib import admin
from .models import Profile, Project


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'role',
        'contact_number',
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'start_date',
        'end_date',
    )

    filter_horizontal = (
        'team_members',
    )