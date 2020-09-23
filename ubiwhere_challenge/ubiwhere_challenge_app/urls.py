from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from rest_framework import routers


urlpatterns = [
    # API VIEWS
    path('api/occurence/', views.OccurenceView.as_view()),

    # BASE VIEWS
    path('', views.index, name='index'),
]