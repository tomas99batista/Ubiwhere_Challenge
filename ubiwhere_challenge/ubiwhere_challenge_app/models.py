from django.contrib.gis.db import models
from django.contrib.auth.models import User
from enum import Enum

# Create your models here.
class Occurence(models.Model):
    # ID
    occurence_id = models.AutoField(primary_key=True)
    
    # Description with no chars limit
    description = models.TextField()
    
    # PostGis
    # https://www.youtube.com/watch?v=vesf9A2PA44&ab_channel=PeterFlynn
    # https://www.youtube.com/watch?v=ymOdTSKRQBs&ab_channel=BlackManSkill
    geographic_location = models.PointField()
    
    # Django Auth
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Timestamps
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    
    # Enums    
    state = models.CharField(
        max_length=18,
        choices=[(state_tag, state_tag.value) for state_tag in State]
    )
    category = models.CharField(
        max_length=18,
        choices=[(category_tag, category_tag.value) for category_tag in Category]
    )

    def __str__(self):
        return self.occurence_id, self.description, self.geographic_location, self.author, self.state, self.category

# https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
class State(Enum):
    TO_VALIDATE = 'To Validate'
    VALIDATED = 'Validated'
    SOLVED = 'Solved'

class Category(Enum):
    CONSTRUCTION = 'Construction'               # Road works planned events;
    SPECIAL_EVENT = 'Special Event'             # Special events (concerts, fairs, etc.);
    INCIDENT = 'Incident'                       # Accidents or other unexpected events;
    WHEATHER_CONDITION = 'Weather Condition'    # Weather events that affect roads;
    ROAD_CONDITION = 'Road Condition'           # Road states that affect those who drive on them (degraded pavement, holes, etc.).
