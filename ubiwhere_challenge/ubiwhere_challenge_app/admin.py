from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from ubiwhere_challenge_app.models import Occurrence


@admin.register(Occurrence)
class OccurrenceAdmin(OSMGeoAdmin):
    list_display = ("occurrence_id", "geographic_location")
