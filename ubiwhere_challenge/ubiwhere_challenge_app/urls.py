from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    # --- API URLS ---
    # POST: Add Occurrence ✔️
    path('api/occurrence/', views.add_new_occurrence, name="add_new_occurrence"),

    # PATCH: Update given Occurrence | ✔️
    # DELETE: Delete given occurrence | ✔️
    # GET: Retrieve given Occurrence by ID ✔️
    path('api/occurrence/<int:pk>/', views.update_delete_get_occurrence, name="update_delete_get_occurrence"),

    # GET: Filter occurrence by author/category/distance to given point ✔️
    path('api/occurrence/filter/', views.filter_occurrences, name="filter_occurrences"),

    # GET: Get all occurrences ✔️
    path('api/occurrence/all/', views.get_all_occurrences, name="get_all_occurrences"),

    # --- AUTH URLS ---
    # POST: Login, retrieve Token ✔️
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    # POST: Register a new user ✔️
    path('api/register/', views.user_register, name="user_register"),
    # GET: Returns all users ✔️
    path('api/users/', views.retrieve_all_users, name="retrieve_all_users"),
    # GET: Get user by ID | ✔️
    # DELETE: Delete given User (by ID) - only allowed by superusers ✔️
    path('api/user/<int:pk>/', views.get_delete_user, name="get_delete_user"),


    # BASE VIEWS
    path('', views.index, name='index'),
]