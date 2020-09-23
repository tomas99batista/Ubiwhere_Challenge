from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from ubiwhere_challenge_app.models import Occurence

@admin.register(Occurence)
class OccurenceAdmin(OSMGeoAdmin):
    list_display = ('occurence_id', 'geographic_location')