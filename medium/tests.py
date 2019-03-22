from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory

from . import models


class PostTests(APITestCase):
    post_create_url = reverse("post-list")
    post_list_url = reverse("post-list")

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.get_or_create(username="testuser")[0]
        test_user_profile = models.UserProfile.objects.create(user=test_user)
        cls.test_user = test_user
        cls.test_user_profile = test_user_profile

    def test_creating_post_with_unauthenticated_user_should_return_401(self):
        response = self.client.post(self.post_create_url, {})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_posts_with_unauthenticated_user_should_return_200(self):
        response = self.client.get(self.post_list_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_creating_post_with_authenticated_user_shoud_return_201(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(
            self.post_create_url, {"title": "The Title", "text": "The Text"}
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class PostsReallySavedTests(APITestCase):
    """This test needs separate class because there is not force_unauthenticate method provided"""

    post_create_url = reverse("post-list")
    post_list_url = reverse("post-list")

    def setUp(self):
        test_user = get_user_model().objects.get_or_create(username="testuser")[0]
        test_user_profile = models.UserProfile.objects.create(user=test_user)
        self.client.force_authenticate(user=test_user)
        self.client.post(
            self.post_create_url, {"title": "The Title 1", "text": "The Text 1"}
        )
        self.client.post(
            self.post_create_url, {"title": "The Title 2", "text": "The Text 2"}
        )

    def test_both_posts_are_returned(self):
        response = self.client.get(self.post_list_url)
        self.assertEqual(2, len(response.data))

    def test_titles_are_right(self):
        response = self.client.get(self.post_list_url)
        self.assertTrue("The Title " in response.data[0]["title"])
        self.assertTrue("The Title " in response.data[1]["title"])

    def test_texts_are_right(self):
        response = self.client.get(self.post_list_url)
        self.assertTrue("The Text " in response.data[0]["text"])
        self.assertTrue("The Text " in response.data[1]["text"])

    def test_creation_dates_are_right(self):
        # TODO
        pass


class PostLikeTests(APITestCase):

    post_create_url = reverse("post-list")
    post_list_url = reverse("post-list")

    def setUp(self):
        self.test_user = get_user_model().objects.get_or_create(username="testuser")[0]
        test_user_profile = models.UserProfile.objects.create(user=self.test_user)
        post = models.Post.objects.create(
            title="The Title 1", text="The Text 1", author=test_user_profile
        )
        self.post_toggle_like_url = reverse("post-like", args=(post.id,))

    def test_liking_post_with_unauthenticated_user_should_return_401(self):
        response = self.client.post(self.post_toggle_like_url)
        # TODO: specify only one acceptable status code later
        self.assertTrue(
            response.status_code
            in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

    def test_liking_post_with_authenticated_user_should_return_200(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.post_toggle_like_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    # def test_liking_post_second_time_should_return_400(self):
    #     self.client.force_authenticate(user=self.test_user)
    #     self.client.post(self.post_toggle_like_url)
    #     response = self.client.post(self.post_toggle_like_url)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
