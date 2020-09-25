from rest_framework import serializers
from .models import Occurrence
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.auth.models import User


# The serializer for the Occurrence model
# Takes all fields
# Used to filter search
class OccurrenceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Occurrence
        geo_field = "geographic_location"
        fields = (
            "occurrence_id",
            "description",
            "creation_timestamp",
            "update_timestamp",
            "state",
            "category",
            "author",
        )


# On the creation the inputs are:
#   - description
#   - category
#   - geographic_location
class OccurrenceCreationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Occurrence
        geo_field = "geographic_location"
        fields = ("description", "category")


# On the update/patch the inputs are:
#   - occurrence_id
#   - state
class OccurrencePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        fields = ("occurrence_id", "state")


class CreateUserSerializer(serializers.ModelSerializer):
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "is_superuser")
