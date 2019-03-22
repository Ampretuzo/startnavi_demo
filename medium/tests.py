from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory

from . import models


class PostTests(APITestCase):
    post_create_url = reverse("post-list")

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.get_or_create(username="testuser")[0]
        test_user_profile = models.UserProfile.objects.create(user=test_user)
        cls.test_user = test_user
        cls.test_user_profile = test_user_profile

    def test_creating_post_with_unauthenticated_user_should_return_401(self):
        response = self.client.post(self.post_create_url, {})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_creating_post_with_authenticated_user_shoud_return_201(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(
            self.post_create_url, {"title": "The Title", "text": "The Text"}
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
