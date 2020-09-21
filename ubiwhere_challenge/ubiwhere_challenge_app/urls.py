from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ubiwhere_challenge_app import views

urlpatterns = [
    # BASE VIEWS
    path('', views.index, name='index'),
]