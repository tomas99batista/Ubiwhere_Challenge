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

    # --- OCCURRENCES TESTS ---

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
                "longitude": 40,
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
                "longitude": 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # Patch Occurrence as normal user
    def test_patch_occurrence_normal_user(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # First add the Occurrence
        url = reverse("add_new_occurrence")
        resp_occurr_creation = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude": 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEquals(resp_occurr_creation.status_code, status.HTTP_201_CREATED)

        # Patch the occurrence
        url = "/api/occurrence/" + str(resp_occurr_creation.data["occurrence_id"]) + "/"
        resp = self.client.patch(url, data={"state": "Validated"}, format="json")

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # Delete Occurrence as normal user
    def test_delete_occurrence_normal_user(self):
        self.login_super_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_user_token)

        # First add the Occurrence
        url = reverse("add_new_occurrence")
        resp_occurr_creation = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude": 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEquals(resp_occurr_creation.status_code, status.HTTP_201_CREATED)

        # Now login as normal user, which is not the author
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # Delete the occurrence
        url = "/api/occurrence/" + str(resp_occurr_creation.data["occurrence_id"]) + "/"
        resp = self.client.delete(url, data={"state": "Validated"}, format="json")

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # Delete Occurrence as super user
    def test_delete_occurrence_super_user(self):
        self.login_super_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.super_user_token)

        # First add the Occurrence
        url = reverse("add_new_occurrence")
        resp_occurr_creation = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude": 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEquals(resp_occurr_creation.status_code, status.HTTP_201_CREATED)

        # Delete the occurrence
        url = "/api/occurrence/" + str(resp_occurr_creation.data["occurrence_id"]) + "/"
        resp = self.client.delete(url, data={"state": "Validated"}, format="json")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    # Delete Occurrence as author
    def test_delete_occurrence_author(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # First add the Occurrence
        url = reverse("add_new_occurrence")
        resp_occurr_creation = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude": 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEquals(resp_occurr_creation.status_code, status.HTTP_201_CREATED)

        # Delete the occurrence
        url = "/api/occurrence/" + str(resp_occurr_creation.data["occurrence_id"]) + "/"
        resp = self.client.delete(url, data={"state": "Validated"}, format="json")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    # Get Occurrence
    def test_get_occurrence(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # First add the Occurrence
        url = reverse("add_new_occurrence")
        resp_occurr_creation = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude": 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEquals(resp_occurr_creation.status_code, status.HTTP_201_CREATED)

        # Get the occurrence
        url = "/api/occurrence/" + str(resp_occurr_creation.data["occurrence_id"]) + "/"
        resp = self.client.get(url, format="json")

        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

    # Get Occurrence Not Created
    def test_get_occurrence_not_created(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # Get the occurrence
        url = "/api/occurrence/1000000001/"
        resp = self.client.get(url, format="json")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # Get All Occurrences
    def test_get_all_occurrences(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # First add the Occurrence
        url = reverse("add_new_occurrence")
        resp_occurr_creation = self.client.post(
            url,
            {
                "description": "Teste Add Occurrence",
                "category": "Construction",
                "longitude": 40,
                "latitude": -7,
            },
            format="json",
        )
        self.assertEquals(resp_occurr_creation.status_code, status.HTTP_201_CREATED)

        # Get the occurrence
        url = reverse("get_all_occurrences")
        resp = self.client.get(url, format="json")

        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

    # Get All Occurrences without having them
    def test_get_all_occurrences_failure(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # Get the occurrence
        url = reverse("get_all_occurrences")
        resp = self.client.get(url, format="json")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    # --- AUTH TESTS ---

    # Get all Users
    def test_get_all_users(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # Get the occurrence
        url = reverse("get_all_users")
        resp = self.client.get(url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

    # Get user by ID
    def test_get_user_by_id(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # Get the occurrence
        url = reverse("get_all_users")
        resp = self.client.get(url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

        user_id = resp.data[0]["id"]

        # Get the occurrence
        url = "/api/user/" + str(user_id) + "/"
        resp = self.client.get(url, format="json")

        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

    # Get user by ID - Failure
    def test_get_user_by_id_not_found(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # Get the occurrence
        url = "/api/user/10000000/"
        resp = self.client.get(url, format="json")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # Delete User as normal user
    def test_delete_user_as_normal_user(self):
        self.login_normal_user()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.normal_user_token)

        # Get the occurrence
        url = reverse("get_all_users")
        resp = self.client.get(url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

        user_id = resp.data[0]["id"]

        # Get the occurrence
        url = "/api/user/" + str(user_id) + "/"
        resp = self.client.delete(url, format="json")

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

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
