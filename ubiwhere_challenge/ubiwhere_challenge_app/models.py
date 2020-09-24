from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Occurrence(models.Model):

    class State(models.TextChoices):
        TO_VALIDATE = 'To Validate'
        VALIDATED = 'Validated'
        SOLVED = 'Solved'

    class Category(models.TextChoices):
        CONSTRUCTION = 'Construction'               # Road works planned events;
        SPECIAL_EVENT = 'Special Event'             # Special events (concerts, fairs, etc.);
        INCIDENT = 'Incident'                       # Accidents or other unexpected events;
        WHEATHER_CONDITION = 'Weather Condition'    # Weather events that affect roads;
        ROAD_CONDITION = 'Road Condition'           # Road states that affect those who drive on them (degraded pavement, holes, etc.).

    # ID
    occurrence_id = models.AutoField(primary_key=True)
    
    # Description with no chars limit
    description = models.TextField(null=False, blank=True)
    
    # PostGis POINT(X Y)
    # https://www.youtube.com/watch?v=vesf9A2PA44&ab_channel=PeterFlynn
    # https://www.youtube.com/watch?v=ymOdTSKRQBs&ab_channel=BlackManSkill
    geographic_location = models.PointField(blank=True)
    
    # Django Auth
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Timestamps of creation and update
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    
    # Enums    
    # State (To Validate, Validated, Solved)
    state = models.CharField(
        max_length=18,
        choices=State.choices,
        default=State.TO_VALIDATE
    )
    # Category (Construction, Special Event, Incident, Wheather Condition, Road Condition)
    category = models.CharField(
        max_length=18,
        choices=Category.choices,
        null=False, blank=True
    )

    def __str__(self):
        return f"ID: {self.occurrence_id}, Description: {self.description}, Location: {self.geographic_location}, Author: {self.author.username}, State: {self.get_state_display()}, Category: {self.get_category_display()}, Creation: {self.creation_timestamp}, Update: {self.update_timestamp}"
