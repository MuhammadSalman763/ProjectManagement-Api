from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationAPITestCase(APITestCase):
    # Ticket 1: User Registration API - API test suite
    url = '/api/register/'

    def test_user_can_register(self):
        data = {
            'username': 'salman',
            'email': 'salman@example.com',
            'password': 'StrongPass123',
            'role': 'developer',
            'contact_number': '03001234567',
        }

        response = self.client.post(self.url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            User.objects.filter(username='salman').exists()
        )

        user = User.objects.get(username='salman')

        self.assertTrue(
            hasattr(user, 'profile')
        )

        self.assertEqual(
            user.profile.role,
            'developer'
        )

        self.assertEqual(
            user.profile.contact_number,
            '03001234567'
        )

        self.assertTrue(
            user.check_password('StrongPass123')
        )

    def test_user_can_register_with_profile_picture(self):
        # Ticket 1: Test profile picture upload
        image = BytesIO()

        Image.new(
            'RGB',
            (100, 100),
            color='white'
        ).save(
            image,
            format='JPEG'
        )

        image.seek(0)

        profile_picture = SimpleUploadedFile(
            'profile.jpg',
            image.read(),
            content_type='image/jpeg'
        )

        data = {
            'username': 'pictureuser',
            'email': 'picture@example.com',
            'password': 'StrongPass123',
            'role': 'developer',
            'contact_number': '03001234567',
            'profile_picture': profile_picture,
        }

        response = self.client.post(
            self.url,
            data,
            format='multipart'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        user = User.objects.get(
            username='pictureuser'
        )

        self.assertTrue(
            user.profile.profile_picture
        )

        self.assertTrue(
            user.profile.profile_picture.name.startswith(
                'profile_pictures/'
            )
        )

        self.assertIsNotNone(
            response.data['user']['profile_picture']
        )

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(
            username='salman',
            email='old@example.com',
            password='StrongPass123'
        )

        data = {
            'username': 'salman',
            'email': 'new@example.com',
            'password': 'StrongPass123',
            'role': 'developer',
        }

        response = self.client.post(
            self.url,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            username='existing',
            email='salman@example.com',
            password='StrongPass123'
        )

        data = {
            'username': 'newuser',
            'email': 'salman@example.com',
            'password': 'StrongPass123',
            'role': 'developer',
        }

        response = self.client.post(
            self.url,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_short_password_is_rejected(self):
        data = {
            'username': 'salman',
            'email': 'salman@example.com',
            'password': '123',
            'role': 'developer',
        }

        response = self.client.post(
            self.url,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_invalid_role_is_rejected(self):
        data = {
            'username': 'salman',
            'email': 'salman@example.com',
            'password': 'StrongPass123',
            'role': 'invalid_role',
        }

        response = self.client.post(
            self.url,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_required_username_is_validated(self):
        data = {
            'email': 'salman@example.com',
            'password': 'StrongPass123',
            'role': 'developer',
        }

        response = self.client.post(
            self.url,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )