from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from PIL import Image

from rest_framework import status
from rest_framework.test import APITestCase

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


class BaseAPITestCase(APITestCase):

    def create_user(
        self,
        username="salman767",
        email="salman@example.com",
        password="Salman12345",
        role="developer",
    ):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        Profile.objects.create(
            user=user,
            role=role,
        )

        return user

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def create_project(self, user=None):
        project = Project.objects.create(
            title="Test Project",
            description="Test project description",
            start_date="2026-08-25",
            end_date="2026-09-25",
        )

        if user:
            project.team_members.add(user)

        return project

    def create_task(self, project, assignee=None):
        return Task.objects.create(
            title="Test Task",
            description="Test task description",
            status="open",
            project=project,
            assignee=assignee,
        )

    def create_document(self, project):
        file_data = SimpleUploadedFile(
            "test.txt",
            b"This is a test document.",
            content_type="text/plain",
        )

        return Document.objects.create(
            name="Test Document",
            description="Test document description",
            file=file_data,
            version="1.0",
            project=project,
        )

    def create_image(self):
        image = Image.new(
            "RGB",
            (100, 100),
            color="white",
        )

        image_io = BytesIO()
        image.save(
            image_io,
            format="JPEG",
        )

        image_io.seek(0)

        return SimpleUploadedFile(
            "profile.jpg",
            image_io.read(),
            content_type="image/jpeg",
        )


# ============================================================
# TICKET 1 - USER REGISTRATION
# ============================================================

class Ticket01RegistrationTests(BaseAPITestCase):

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "TestPassword123",
            "role": "developer",
            "contact_number": 3001234567,
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                username="newuser"
            ).exists()
        )

        user = User.objects.get(
            username="newuser"
        )

        self.assertTrue(
            Profile.objects.filter(
                user=user
            ).exists()
        )

    def test_registration_with_profile_picture(self):
        data = {
            "username": "pictureuser",
            "email": "picture@example.com",
            "password": "TestPassword123",
            "role": "developer",
            "contact_number": 3001234567,
            "profile_picture": self.create_image(),
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(
            username="pictureuser"
        )

        profile = Profile.objects.get(
            user=user
        )

        self.assertTrue(
            bool(profile.profile_picture)
        )


# ============================================================
# TICKET 2 - USER LOGIN
# ============================================================

class Ticket02LoginTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "salman767",
                "password": "Salman12345",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "refresh",
            response.data,
        )

        self.assertEqual(
            response.data["user"]["username"],
            "salman767",
        )

        self.assertEqual(
            response.data["user"]["role"],
            "developer",
        )

    def test_invalid_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "salman767",
                "password": "WrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


# ============================================================
# TICKET 3 - USER LOGOUT
# ============================================================

class Ticket03LogoutTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.refresh_token = str(
            RefreshToken.for_user(self.user)
        )

        self.authenticate(self.user)

    def test_user_logout(self):
        response = self.client.post(
            reverse("logout"),
            {
                "refresh": self.refresh_token,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "User logged out successfully.",
        )

    def test_logout_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.post(
            reverse("logout"),
            {
                "refresh": self.refresh_token,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


# ============================================================
# TICKET 4 - CREATE PROJECT
# ============================================================

class Ticket04ProjectCreateTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user(
            role="manager"
        )

        self.authenticate(self.user)

    def test_create_project(self):
        data = {
            "title": "New Project",
            "description": "New project description",
            "start_date": "2026-08-25",
            "end_date": "2026-09-25",
        }

        response = self.client.post(
            reverse("project-create"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        project = Project.objects.get(
            title="New Project"
        )

        self.assertTrue(
            project.team_members.filter(
                id=self.user.id
            ).exists()
        )

        self.assertTrue(
            TimelineEvent.objects.filter(
                project=project,
                user=self.user,
                event_type="project_created",
            ).exists()
        )


# ============================================================
# TICKET 5 - LIST PROJECTS
# ============================================================

class Ticket05ProjectListTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user(
            role="manager"
        )

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

    def test_list_projects(self):
        response = self.client.get(
            reverse("project-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_project_list_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse("project-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


# ============================================================
# TICKET 6 - PROJECT DETAIL
# ============================================================

class Ticket06ProjectDetailTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user(
            role="manager"
        )

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

    def test_project_detail(self):
        response = self.client.get(
            reverse(
                "project-detail",
                kwargs={
                    "pk": self.project.id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 7 - PROJECT UPDATE
# ============================================================

class Ticket07ProjectUpdateTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user(
            role="manager"
        )

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

    def test_project_update(self):
        response = self.client.put(
            reverse(
                "project-update",
                kwargs={
                    "pk": self.project.id
                },
            ),
            {
                "title": "Updated Project",
                "description": "Updated description",
                "start_date": "2026-08-25",
                "end_date": "2026-10-25",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.project.refresh_from_db()

        self.assertEqual(
            self.project.title,
            "Updated Project",
        )


# ============================================================
# TICKET 8 - PROJECT DELETE
# ============================================================

class Ticket08ProjectDeleteTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user(
            role="manager"
        )

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

    def test_project_delete(self):
        project_id = self.project.id

        response = self.client.delete(
            reverse(
                "project-delete",
                kwargs={
                    "pk": project_id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            Project.objects.filter(
                id=project_id
            ).exists()
        )


# ============================================================
# TICKET 9 - CREATE TASK
# ============================================================

class Ticket09TaskCreateTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user(
            role="developer"
        )

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

    def test_create_task(self):
        response = self.client.post(
            reverse("task-create"),
            {
                "title": "New Task",
                "description": "Task description",
                "status": "open",
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Task.objects.filter(
                title="New Task"
            ).exists()
        )


# ============================================================
# TICKET 10 - LIST TASKS
# ============================================================

class Ticket10TaskListTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.task = self.create_task(
            self.project,
            self.user,
        )

    def test_task_list(self):
        response = self.client.get(
            reverse("task-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 11 - TASK DETAIL
# ============================================================

class Ticket11TaskDetailTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.task = self.create_task(
            self.project,
            self.user,
        )

    def test_task_detail(self):
        response = self.client.get(
            reverse(
                "task-detail",
                kwargs={
                    "pk": self.task.id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 12 - UPDATE TASK
# ============================================================

class Ticket12TaskUpdateTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.task = self.create_task(
            self.project,
            self.user,
        )

    def test_task_update(self):
        response = self.client.put(
            reverse(
                "task-update",
                kwargs={
                    "pk": self.task.id
                },
            ),
            {
                "title": "Updated Task",
                "description": "Updated task description",
                "status": "working",
                "project": self.project.id,
                "assignee": self.user.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.title,
            "Updated Task",
        )

        self.assertEqual(
            self.task.status,
            "working",
        )


# ============================================================
# TICKET 13 - DELETE TASK
# ============================================================

class Ticket13TaskDeleteTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.task = self.create_task(
            self.project,
            self.user,
        )

    def test_task_delete(self):
        task_id = self.task.id

        response = self.client.delete(
            reverse(
                "task-delete",
                kwargs={
                    "pk": task_id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            Task.objects.filter(
                id=task_id
            ).exists()
        )


# ============================================================
# TICKET 14 - ASSIGN TASK
# ============================================================

class Ticket14TaskAssignTests(BaseAPITestCase):

    def setUp(self):
        self.manager = self.create_user(
            username="manager",
            email="manager@example.com",
            role="manager",
        )

        self.assignee = self.create_user(
            username="developer",
            email="developer@example.com",
            role="developer",
        )

        self.authenticate(self.manager)

        self.project = self.create_project(
            self.manager
        )

        self.project.team_members.add(
            self.assignee
        )

        self.task = self.create_task(
            self.project
        )

    def test_assign_task(self):
        response = self.client.post(
            reverse(
                "task-assign",
                kwargs={
                    "pk": self.task.id
                },
            ),
            {
                "assignee": self.assignee.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.assignee,
            self.assignee,
        )

        self.assertTrue(
            Notification.objects.filter(
                user=self.assignee,
                message__icontains=self.task.title,
            ).exists()
        )

        self.assertTrue(
            TimelineEvent.objects.filter(
                project=self.project,
                event_type="task_assigned",
            ).exists()
        )


# ============================================================
# TICKET 15 - UPLOAD DOCUMENT
# ============================================================

class Ticket15DocumentUploadTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

    def test_document_upload(self):
        file_data = SimpleUploadedFile(
            "document.txt",
            b"This is test document content.",
            content_type="text/plain",
        )

        response = self.client.post(
            reverse("document-upload"),
            {
                "name": "Test Document",
                "description": "Test document",
                "file": file_data,
                "version": "1.0",
                "project": self.project.id,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Document.objects.filter(
                name="Test Document"
            ).exists()
        )


# ============================================================
# TICKET 16 - LIST DOCUMENTS
# ============================================================

class Ticket16DocumentListTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.document = self.create_document(
            self.project
        )

    def test_document_list(self):
        response = self.client.get(
            reverse("document-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 17 - DOCUMENT DETAIL
# ============================================================

class Ticket17DocumentDetailTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.document = self.create_document(
            self.project
        )

    def test_document_detail(self):
        response = self.client.get(
            reverse(
                "document-detail",
                kwargs={
                    "pk": self.document.id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 18 - UPDATE DOCUMENT
# ============================================================

class Ticket18DocumentUpdateTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.document = self.create_document(
            self.project
        )

    def test_document_update(self):
        response = self.client.patch(
            reverse(
                "document-update",
                kwargs={
                    "pk": self.document.id
                },
            ),
            {
                "name": "Updated Document",
                "description": "Updated description",
                "version": "2.0",
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.name,
            "Updated Document",
        )

        self.assertEqual(
            self.document.version,
            "2.0",
        )


# ============================================================
# TICKET 19 - DELETE DOCUMENT
# ============================================================

class Ticket19DocumentDeleteTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.document = self.create_document(
            self.project
        )

    def test_document_delete(self):
        document_id = self.document.id

        response = self.client.delete(
            reverse(
                "document-delete",
                kwargs={
                    "pk": document_id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            Document.objects.filter(
                id=document_id
            ).exists()
        )


# ============================================================
# TICKET 20 - CREATE COMMENT
# ============================================================

class Ticket20CommentCreateTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.task = self.create_task(
            self.project,
            self.user,
        )

    def test_create_project_comment(self):
        response = self.client.post(
            reverse("comment-create"),
            {
                "text": "Project comment",
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Comment.objects.filter(
                text="Project comment",
                author=self.user,
                project=self.project,
            ).exists()
        )

    def test_create_task_comment(self):
        response = self.client.post(
            reverse("comment-create"),
            {
                "text": "Task comment",
                "task": self.task.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Comment.objects.filter(
                text="Task comment",
                author=self.user,
                task=self.task,
            ).exists()
        )


# ============================================================
# TICKET 21 - LIST COMMENTS
# ============================================================

class Ticket21CommentListTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.task = self.create_task(
            self.project,
            self.user,
        )

        self.comment = Comment.objects.create(
            text="Test comment",
            author=self.user,
            project=self.project,
            task=self.task,
        )

    def test_comment_list(self):
        response = self.client.get(
            reverse("comment-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 22 - UPDATE COMMENT
# ============================================================

class Ticket22CommentUpdateTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.comment = Comment.objects.create(
            text="Old comment",
            author=self.user,
            project=self.project,
        )

    def test_comment_update(self):
        response = self.client.put(
            reverse(
                "comment-update",
                kwargs={
                    "pk": self.comment.id
                },
            ),
            {
                "text": "Updated comment",
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.comment.refresh_from_db()

        self.assertEqual(
            self.comment.text,
            "Updated comment",
        )


# ============================================================
# TICKET 23 - DELETE COMMENT
# ============================================================

class Ticket23CommentDeleteTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.comment = Comment.objects.create(
            text="Delete comment",
            author=self.user,
            project=self.project,
        )

    def test_comment_delete(self):
        comment_id = self.comment.id

        response = self.client.delete(
            reverse(
                "comment-delete",
                kwargs={
                    "pk": comment_id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            Comment.objects.filter(
                id=comment_id
            ).exists()
        )


# ============================================================
# TICKET 24 - COMMENT DETAIL
# ============================================================

class Ticket24CommentDetailTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.comment = Comment.objects.create(
            text="Detail comment",
            author=self.user,
            project=self.project,
        )

    def test_comment_detail(self):
        response = self.client.get(
            reverse(
                "comment-detail",
                kwargs={
                    "pk": self.comment.id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 25 - PROJECT COMMENTS
# ============================================================

class Ticket25ProjectCommentsTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.comment = Comment.objects.create(
            text="Project comment",
            author=self.user,
            project=self.project,
        )

    def test_project_comments(self):
        response = self.client.get(
            reverse(
                "project-comments",
                kwargs={
                    "project_id": self.project.id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 26 - TIMELINE EVENTS
# ============================================================

class Ticket26TimelineTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.authenticate(self.user)

        self.project = self.create_project(
            self.user
        )

        self.event = TimelineEvent.objects.create(
            project=self.project,
            user=self.user,
            event_type="test_event",
            description="Test timeline event",
        )

    def test_timeline_events(self):
        response = self.client.get(
            reverse("timeline-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


# ============================================================
# TICKET 27 - NOTIFICATIONS
# ============================================================

class Ticket27NotificationTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.other_user = self.create_user(
            username="otheruser",
            email="other@example.com",
        )

        self.authenticate(self.user)

        self.notification = Notification.objects.create(
            user=self.user,
            message="My notification",
        )

        self.other_notification = Notification.objects.create(
            user=self.other_user,
            message="Other notification",
        )

    def test_notification_list(self):
        response = self.client.get(
            reverse("notification-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        messages = [
            item["message"]
            for item in response.data
        ]

        self.assertIn(
            "My notification",
            messages,
        )

        self.assertNotIn(
            "Other notification",
            messages,
        )

    def test_notification_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse("notification-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


# ============================================================
# TICKET 28 - MARK NOTIFICATION AS READ
# ============================================================

class Ticket28NotificationReadTests(BaseAPITestCase):

    def setUp(self):
        self.user = self.create_user()

        self.other_user = self.create_user(
            username="otheruser",
            email="other@example.com",
        )

        self.authenticate(self.user)

        self.notification = Notification.objects.create(
            user=self.user,
            message="Unread notification",
            is_read=False,
        )

        self.other_notification = Notification.objects.create(
            user=self.other_user,
            message="Other user's notification",
            is_read=False,
        )

    def test_mark_notification_as_read(self):
        response = self.client.patch(
            reverse(
                "notification-mark-read",
                kwargs={
                    "pk": self.notification.id
                },
            ),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.notification.refresh_from_db()

        self.assertTrue(
            self.notification.is_read
        )

        self.assertEqual(
            response.data["message"],
            "Notification marked as read.",
        )

    def test_cannot_mark_other_users_notification(self):
        response = self.client.patch(
            reverse(
                "notification-mark-read",
                kwargs={
                    "pk": self.other_notification.id
                },
            ),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )