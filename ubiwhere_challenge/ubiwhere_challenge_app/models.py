from django.db import models
from django.contrib.auth.models import User

# === Models for Occurrences ===


class Occurrence(models.Model):

    """

    The Occurrence class defines the class of occurrences
    Each occurrence has  fields:

    """

    class State(models.TextChoices):

        """
        
        Possible state choices:

        """

        TO_VALIDATE = "To Validate"
        VALIDATED = "Validated"
        SOLVED = "Solved"

    class Category(models.TextChoices):
        
        """
        
        Possible Occurrence categories:

        """
        
        CONSTRUCTION = "Construction"  # Road works planned events;
        SPECIAL_EVENT = "Special Event"  # Special events (concerts, fairs, etc.);
        INCIDENT = "Incident"  # Accidents or other unexpected events;
        WHEATHER_CONDITION = "Weather Condition"  # Weather events that affect roads;
        ROAD_CONDITION = "Road Condition"  # Road states that affect those who drive on them (degraded pavement, holes, etc.).

    # **occurrence_id** - unique identifier
    occurrence_id = models.AutoField(primary_key=True)
    # **description** - text description
    description = models.TextField(null=False, blank=True)
    # **geographic_location** - (logintude, latitude)
    # **longitude**
    longitude = models.FloatField(null=False, blank=True)
    # **longitude**
    latitude = models.FloatField(null=False, blank=True)
    # **author** - creator of the occurrence
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # **creation_timestamp** - timestamp of the creation
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    # **update_timestamp** - timestamp of the last update
    update_timestamp = models.DateTimeField(auto_now=True)
    # **state** - actual state
    state = models.CharField(
        max_length=18, choices=State.choices, default=State.TO_VALIDATE
    )
    # **category** - occurrence category
    category = models.CharField(
        max_length=18, choices=Category.choices, null=False, blank=True
    )

    def __str__(self):

        return f"ID: {self.occurrence_id}, Description: {self.description}, Location: ({self.longitude}, {self.latitude}), \
                Author: {self.author.username}, State: {self.get_state_display()}, Category: {self.get_category_display()}, \
                Creation: {self.creation_timestamp}, Update: {self.update_timestamp}"
