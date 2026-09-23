from typing import TypedDict, cast, override

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserResponseData(TypedDict):
    id: int
    email: str
    username: str
    password: str


class UserAPITests(APITestCase):
    @override
    def setUp(self):
        self.user = User.objects.create_user(
            username="johndoe", email="john@example.com", password="old_password"
        )
        self.list_url = "/api/users/"
        self.detail_url = f"/api/users/{cast(int, self.user.pk)}/"

    def test_create_user_hashes_password_and_hides_it(self):
        payload = {
            "username": "new_user",
            "email": "new@example.com",
            "password": "my_super_password",
        }
        response = self.client.post(self.list_url, payload)
        data = cast(UserResponseData, response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", data)

        new_user = User.objects.get(username="new_user")
        self.assertTrue(new_user.check_password("my_super_password"))

    def test_email_must_be_unique_on_create(self):
        payload = {
            "username": "someone_else",
            "email": "john@example.com",  # Used in setUp
            "password": "password123",
        }
        response = self.client.post(self.list_url, payload)
        data = cast(UserResponseData, response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", data)

    def test_user_can_update_own_email(self):
        payload = {"email": "new_john@example.com"}
        response = self.client.patch(self.detail_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new_john@example.com")

    def test_update_password_is_hashed(self):
        payload = {"password": "new_secure_password"}
        response = self.client.patch(self.detail_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_secure_password"))
