from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    """
    Base permission for checking the user's profile role.
    """

    allowed_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        profile = getattr(request.user, "profile", None)

        if profile is None:
            return False

        return profile.role in self.allowed_roles


class IsManager(HasRole):
    """
    Allows managers only.
    """

    allowed_roles = ["manager"]
    message = "Only managers are allowed to perform this action."


class IsManagerOrDeveloper(HasRole):
    """
    Allows managers and developers.
    """

    allowed_roles = ["manager", "developer"]
    message = "Only managers or developers are allowed to perform this action."


class IsManagerOrQA(HasRole):
    """
    Allows managers and QA users.
    """

    allowed_roles = ["manager", "qa"]
    message = "Only managers or QA users are allowed to perform this action."


class IsProjectTeamMember(BasePermission):
    """
    Allows access only to users who are members of the project team.

    Works with:
    - Project
    - Task
    - Document
    """

    message = "You must be a member of the project team."

    def has_object_permission(self, request, view, obj):
        project = None

        # Project
        if hasattr(obj, "team_members"):
            project = obj

        # Task / Document
        elif hasattr(obj, "project"):
            project = obj.project

        if project is None:
            return False

        return project.team_members.filter(
            id=request.user.id
        ).exists()


class IsCommentAuthor(BasePermission):
    """
    Allows access only to the author of a comment.
    """

    message = "You can only modify your own comments."

    def has_object_permission(self, request, view, obj):
        return obj.author_id == request.user.id


class IsNotificationOwner(BasePermission):
    """
    Allows access only to the owner of a notification.
    """

    message = "You can only access your own notifications."

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id