from rest_framework import serializers
from .models import Occurrence
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.auth.models import User

# === Serializers for Occurrences and Users ===

"""
The serializers are used to transform data into python readable to other format and vice-versa.
We have 5 Serializers:
"""

"""
**OccurrenceSerializer** - The main serializer of [[models.py#Occurrence]]
"""


class OccurrenceSerializer(serializers.ModelSerializer):
    """
    Takes in consideration all fields
    Used on:

    - [[views.py#update_delete_get_occurrence]] on GET to serialize requested Occurrence
    - [[views.py#filter_occurrences]] on GET to serialized the filtered Occurrences
    - [[views.py#get_all_occurrences]] on GET to serialize all the Occurrences

    """

    class Meta:
        model = Occurrence
        fields = (
            "occurrence_id",
            "description",
            "creation_timestamp",
            "update_timestamp",
            "state",
            "category",
            "author",
            "longitude", 
            "latitude"
        )


"""
**OccurrenceCreationSerializer** - The serializer for creating Occurrences [[models.py#Occurrence]]
"""


class OccurrenceCreationSerializer(serializers.ModelSerializer):
    """
    Takes in consideration only the geo_field, description and category
    Used on:

    - [[views.py#add_new_occurrence]] on POST to serialize the Occurrence sent to be created

    """

    class Meta:
        model = Occurrence
        fields = ("description", "category", "longitude", "latitude")


"""
**OccurrencePatchSerializer** - The serializer for updating the state of the Occurrences [[models.py#Occurrence]]
"""


class OccurrencePatchSerializer(serializers.ModelSerializer):
    """
    Takes in consideration only the occurrence_id and the state, which is the field to update
    Used on:

    - [[views.py#update_delete_get_occurrence]] on POST to serialize the updated Occurrence object

    """

    class Meta:
        model = Occurrence
        fields = ("occurrence_id", "state")


"""
**CreateUserSerializer** - The serializer for creating the authors of [[models.py#Occurrence]]
"""


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Takes in consideration only the username and the password
    It's not possible to more than the superuser auto-created (admin)
    Used on:

    - [[views.py#user_register]] on POST to serialize the new User

    """

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        user = User(username=username)
        user.set_password(password)
        user.is_superuser = False
        user.save()
        return user


"""
**UserSerializer** - The main serializer of the authors of [[models.py#Occurrence]]
"""


class UserSerializer(serializers.ModelSerializer):
    """
    Takes in consideration only the id, username and if is a superuser
    Used on:

    - [[views.py#retrieve_all_users]] on GET to return all Users
    - [[views.py#get_delete_user]] on GET to return the requested User

    """

    class Meta:
        model = User
        fields = ("id", "username", "is_superuser")
