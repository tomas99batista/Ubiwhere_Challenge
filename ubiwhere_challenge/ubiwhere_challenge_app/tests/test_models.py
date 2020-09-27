from django.test import TestCase
from ubiwhere_challenge_app.models import Occurrence
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

# --- Model Tests ---
print("\nMODELS TESTS\n")
class OccurrenceModelTest(TestCase):    
    def setUp(self):
        self.occurrence = Occurrence.objects.create(description= "Occurence - CONSTRUCTION - initial data, created by a initial user",
                                            geographic_location= "POINT(25 -14)",
                                            author= User.objects.create_user('userteste', 'userteste@example.com', 'userteste'),
                                            category="Construction")
    
    def test_occurrence_fields(self):
        self.assertIsInstance(self.occurrence.description, str)
        self.assertIsInstance(self.occurrence.category, str)
        self.assertIsInstance(self.occurrence.state, str)
    
    def test_occurrence_default_state(self):
        self.assertEqual(self.occurrence.state, "To Validate")

    def test_timestamps(self):
        self.assertIsInstance(self.occurrence.creation_timestamp, datetime)
        self.assertIsInstance(self.occurrence.update_timestamp, datetime)