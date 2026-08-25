from rest_framework.permissions import BasePermission


class IsProjectTeamMember(BasePermission):
    """
    Allows access only to users who are members of the project.
    Works with Project, Task, and Document objects.
    """

    message = "You must be a member of the project team."

    def has_object_permission(self, request, view, obj):
        project = None

        # Project object
        if hasattr(obj, "team_members"):
            project = obj

        # Task object
        elif hasattr(obj, "project") and obj.project is not None:
            project = obj.project

        # Document object
        elif hasattr(obj, "project") and obj.project is not None:
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
        return obj.author == request.user