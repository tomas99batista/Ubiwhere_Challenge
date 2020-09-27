from django.urls import path
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Occurrences API - Ubiwhere Challenge",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# === Serializers for Occurrences and Users ===

"""
The urls are the endpoints to access the API and the index page
We have 9 urls:
"""

urlpatterns = [
    # **API URLS** - The urls for the Occurrence [[models.py#Occurrence]]
    # - **POST: Add Occurrence** - Create a new Occurrence
    path("api/occurrence/", views.add_new_occurrence, name="add_new_occurrence"),
    # - **PATCH: Update one Occurrence** - Updates the state of the Occurrence requested - Only Superusers
    # - **DELETE: Delete one Occurrence** - Deletes the Occurrence requested - Only SuperUsers or Authors
    # - **GET: Get Occurrence By ID** - Gets the Occurrence requested
    path(
        "api/occurrence/<int:pk>/",
        views.update_delete_get_occurrence,
        name="update_delete_get_occurrence",
    ),
    # - **GET: Filter Occurrences** - Gets the Occurrences filtered by author/caregory/distance to given point
    path("api/occurrence/filter/", views.filter_occurrences, name="filter_occurrences"),
    # - **GET: Get All Occurrences** - Retrieves all Occurrences
    path("api/occurrence/all/", views.get_all_occurrences, name="get_all_occurrences"),
    
    # **AUTH URLS** - The urls for the User (author [[models.py#Occurrence]])
    # - **POST: Login** - Retrieves Auth Token
    path("api/login/", jwt_views.TokenObtainPairView.as_view(), name="login"),
    # - **POST: Register** - Register new User
    path("api/register/", views.user_register, name="user_register"),
    # - **GET: Get All Users** - Retrieves all Users
    path("api/user/all/", views.retrieve_all_users, name="retrieve_all_users"),
    # - **GET: Get User By ID** - Retrieves requested User
    # - **DELETE: Delete one User** - Deletes requested User - Only SuperUsers
    path("api/user/<int:pk>/", views.get_delete_user, name="get_delete_user"),
    # **TEMPLATE URLS** - The URLS for HTML pages
    path("", views.index, name="index"),
    
    # Swagger URLS   
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
