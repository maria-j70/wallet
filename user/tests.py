from django.test import TestCase
from rest_framework.test import APIClient

from wallet import factories


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = factories.UserFactory.create()

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', {
            "username": "user_name",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email@example.com",
            "password": "password"
        })

        expected_response = {
            'username': 'user_name',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@example.com'
        }

        response_dict = response.json()

        self.assertIn("id", response_dict)
        response_dict.pop('id')
        self.assertEqual(response.status_code, 201)
        self.maxDiff = None
        self.assertEqual(response.json(), expected_response)

    def test_user_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/users/detail')
        expected_response = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email
        }

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(response.json(), expected_response)
