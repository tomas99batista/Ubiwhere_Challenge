from rest_framework.test import APITestCase
from ubiwhere_challenge_app.models import Occurrence

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

# --- API Tests ---
print("\nAPI TESTS\n")


class OccurrenceAPITest(APITestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user(
            username="normal_user_tests",
            email="normal_user_tests@example.com",
            password="normal_user_tests",
        )
        self.super_user = User.objects.create_user(
            username="super_user_tests",
            email="super_user_tests@example.com",
            password="super_user_tests",
        )
        self.normal_user_token = ""
        self.super_user_token = ""

    # Get Token for normal user
    def login_normal_user(self):
        url = reverse("login")
        resp = self.client.post(
            url,
            {"username": "normal_user_tests", "password": "normal_user_tests"},
            format="json",
        )
        self.normal_user_token = resp.data["access"]

    # Get Token for super user
    def login_super_user(self):
        url = reverse("login")
        resp = self.client.post(
            url,
            {"username": "super_user_tests", "password": "super_user_tests"},
            format="json",
        )
        self.super_user_token = resp.data["access"]

    # Test Good Registration
    def test_registration(self):
        url = reverse("user_register")
        resp = self.client.post(
            url,
            {"username": "user_register", "password": "user_register"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    # Test Bad Registration - Missing username field
    def test_bad_registration_missing_fields(self):
        url = reverse("user_register")
        resp = self.client.post(url, {"password": "user_register"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # Create Occurrence Authenticated
    def test_add_occurrence_authenticated(self):
        self.login_super_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_user_token)
        url = reverse("add_new_occurrence")
        resp = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude" : 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    # Create Bad Occurrence - Withouth authentication
    def test_add_occurrence_without_authentication(self):
        url = reverse("add_new_occurrence")
        resp = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude" : 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # Patch Occurrence as Super User
    def test_patch_occurrence_super_user(self):
        self.login_super_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_user_token)

        # First add the Occurrence
        url = reverse("add_new_occurrence")
        resp = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude" : 40,
                "latitude": -7,
            },
            format="json",
        )

        resp = self.client.get(reverse("get_all_occurrences"), format="json")
        print(resp.data)

        resp = self.client.patch(
            "api/occurrence/5/", data={"state": "Validated"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
