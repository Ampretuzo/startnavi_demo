from unittest.mock import Mock, patch

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
        self.post_like_url = reverse("post-like", args=(post.id,))
        self.post_unlike_url = reverse("post-unlike", args=(post.id,))

    def test_liking_post_with_unauthenticated_user_should_return_4xx(self):
        response = self.client.post(self.post_like_url)
        # TODO: specify only one acceptable status code later
        self.assertTrue(
            response.status_code
            in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

    def test_liking_post_with_authenticated_user_should_return_200(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.post_like_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_liking_post_second_time_should_return_400(self):
        self.client.force_authenticate(user=self.test_user)
        self.client.post(self.post_like_url)
        response = self.client.post(self.post_like_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_unliking_post_with_unauthenticated_user_should_return_4xx(self):
        response = self.client.post(self.post_unlike_url)
        self.assertTrue(
            response.status_code
            in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        )

    def test_unliking_not_yet_liked_post_with_authenticated_user_should_return_400(
        self
    ):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.post_unlike_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_unliking_liked_post_with_authenticated_user_should_return_200(self):
        self.client.force_authenticate(user=self.test_user)
        self.client.post(self.post_like_url)
        response = self.client.post(self.post_unlike_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_liking_unliked_post_with_authenticated_user_should_return_200(self):
        self.client.force_authenticate(user=self.test_user)
        self.client.post(self.post_like_url)
        self.client.post(self.post_unlike_url)
        response = self.client.post(self.post_like_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class RegistrationTestdrive(APITestCase):
    """This is not a real test, I just made sure libraries are sort
    of working"""

    register_url = reverse("register")
    token_obtain_pair_url = reverse("token_obtain_pair")

    def test_registration_with_no_email_responds_with_400(self):
        response = self.client.post(
            self.register_url, {"username": "testuser", "password": "testuserpassword"}
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_registration_with_valid_data_responds_with_200(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "password": "testuserpassword",
                "email": "testuser@testdomain.com",
            },
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_registered_user_can_get_jwt_token(self):
        self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "password": "testuserpassword",
                "email": "testuser@testdomain.com",
            },
        )
        response = self.client.post(
            self.token_obtain_pair_url,
            {"username": "testuser", "password": "testuserpassword"},
        )
        self.assertTrue("eyJ" in response.data["access"])


class ClearbitEnrichmentTests(APITestCase):

    register_url = reverse("register")

    @patch("clearbit.Enrichment.find")
    def test_enrichment_basic_should_work(self, mock_enrichment_find):
        mock_enrichment_find.return_value = {
            "person": {"name": {"givenName": "Alex", "familyName": "McCaw"}}
        }
        self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "password": "testuserpassword",
                "email": "alex@clearbit.com",
            },
        )
        ued = models.UserEnrichmentData.objects.all()[0]
        self.assertTrue(ued.enrichment_run)
        self.assertEqual(
            mock_enrichment_find.return_value["person"]["name"]["givenName"],
            ued.first_name,
        )
        self.assertEqual(
            mock_enrichment_find.return_value["person"]["name"]["familyName"],
            ued.last_name,
        )
        self.assertEqual("", ued.country)
        mock_enrichment_find.assert_called_once()
