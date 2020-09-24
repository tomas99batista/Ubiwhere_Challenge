from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    # API URLS
    path('api/occurrence/', views.add_new_occurrence, name="add_new_occurrence"),
    path('api/occurrence/<int:pk>/', views.update_occurrence, name="update_occurrence"),
    path('api/occurrence/filter/', views.filter_occurences, name="filter_occurences"),
    path('api/occurrence/all/', views.get_all_occurrences, name="get_all_occurrences"),

    # AUTH URLS
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('api/register/', views.user_register, name="user_register"),
    path('api/users/', views.retrieve_all_users, name="retrieve_all_users"),


    # BASE VIEWS
    path('', views.index, name='index'),
]