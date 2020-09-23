from rest_framework import serializers
from .models import Occurence
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class OccurenceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Occurence
        geo_field = 'geographic_location'
        fields = ('occurence_id', 'description', 'state', 'category')