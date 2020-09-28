from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry

from .serializers import (
    OccurrenceCreationSerializer,
    CreateUserSerializer,
    UserSerializer,
    OccurrenceSerializer,
    OccurrencePatchSerializer,
)
from .models import Occurrence

"""
All the @api_view for our application
We have 6 views:

1. **occurrences_view** 
    - POST a new Occurrence [[views.py#add_new_occurrence]]
    - GET All Occurrences [[views.py#add_new_occurrence]]
    - GET ?filter=value filter Occurrences [[views.py#add_new_occurrence]]
2. **occurrences_by_id_view** - PATCH/DELETE/GET a requested Occurrence [[views.py#update_delete_get_occurrence]]
3. **user_register_view** - POST Register a new User [[views.py#user_register]]
4. **get_all_users_view** - GET all Users [[views.py#retrieve_all_users]]
5. **user_by_id_view** - GET/DELETE requested User [[views.py#get_delete_user]]
6. **Index Page** - returns a webpage with a table to consult all endpoints, how to call, parameters, return and permissions [[views.py#index]]

 === Add New Occurence ===

"""


@swagger_auto_schema(method="post", request_body=OccurrenceCreationSerializer)
@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def occurrences_view(request):

    """

    View to add a new occurrence
    Only allowed to Authenticated Users, which will be the authors of the Occurence
    """
    user = request.user
    if request.method == "POST":
        serializer = OccurrenceCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """

    View where is possible to filter the Occurences pretended by:

    - author: passing the username
    - category: from the valid ones
    - distance: passing a POINT(longitude latitude) and the range pretended from that point

    If no filter is passed, ALL occurrences are returned
    
    Only allowed to Authenticated Users.
    """

    if request.method == "GET":

        queryset = Occurrence.objects.all()

        # Filter by category
        category = request.query_params.get("category", None)
        queryset = (
            queryset.filter(category=category) if category is not None else queryset
        )

        # Filter by author
        username = request.query_params.get("username", None)
        queryset = (
            queryset.filter(author__username=username)
            if username is not None
            else queryset
        )

        # Filter by distance
        latitude = request.query_params.get("latitude", None)
        longitude = request.query_params.get("longitude", None)
        distance_range = request.query_params.get("range", None)
        # If the 3 arguments to the distance filter are passed
        if latitude or longitude or distance_range:
            # If not all 3 (latitude, longitude and distance) distance filters are passed.
            # an bad request error is generated
            if not latitude and not longitude and not distance_range:
                return Response(
                    "BAD REQUEST: Distance filter needs a latitude, a longitude and a distance range.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Create a point from the given longitude and latitude
            point_request = GEOSGeometry(
                "POINT(" + str(longitude) + " " + str(latitude) + ")", srid=4326
            )
            for occurrence in queryset:
                # Creates Point with the help of GEOS
                point_database = GEOSGeometry(
                    "POINT("
                    + str(occurrence.longitude)
                    + " "
                    + str(occurrence.latitude)
                    + ")",
                    srid=4326,
                )
                # Calculate the distance from the stored point to the given point
                distance = point_database.distance(point_request)
                # If the distance from the given point to the stored point is bigger than the distance passed, exclude that point
                queryset = (
                    queryset.exclude(occurrence_id=occurrence.occurrence_id)
                    if distance > float(distance_range)
                    else queryset
                )

        if not queryset:
            return Response(
                "No data found for the given filters", status=status.HTTP_404_NOT_FOUND
            )

        # If no type of filter (category, distance or author) is passed, RETURN ALL
        if (
            not category
            and not latitude
            and not longitude
            and not distance_range
            and not username
        ):
            occurrences = Occurrence.objects.all()
            if not occurrences:
                return Response(
                    "No data on occurrences", status=status.HTTP_404_NOT_FOUND
                )
            serializer = OccurrenceSerializer(occurrences, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = OccurrenceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# === Update/Delete/Get Occurence X ===
@swagger_auto_schema(method="patch", request_body=OccurrencePatchSerializer)
@api_view(["PATCH", "DELETE", "GET"])
@permission_classes([IsAuthenticated])
def occurrences_by_id_view(request, pk):

    """

    View where is possible to update, delete or get a given Occurrence, passing the
    primary key through the url
    Only allowed to Authenticated Users. Only superusers or the authors
    of the Occurrence are allowed to delete. Only superusers are authorized
    to update the Occurrence (and only the state is updatable)
    """

    if request.method == "PATCH":
        user = request.user
        if not user.is_superuser:
            return Response(
                "Only superusers are allowed to update occurrences",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=pk)
        serializer = OccurrencePatchSerializer(
            occurrence, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        user = request.user
        occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=pk)
        # Superuser or author can delete instance
        if occurrence.author == user or user.is_superuser:
            occurrence.delete()
            return Response("Occurrence deleted", status=status.HTTP_200_OK)
        else:
            return Response(
                "Only superusers or creators allowed to delete occurrences",
                status=status.HTTP_401_UNAUTHORIZED,
            )
    if request.method == "GET":
        occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=pk)
        serializer = OccurrenceSerializer(occurrence)
        return Response(serializer.data, status=status.HTTP_200_OK)


# === Register User ===
@swagger_auto_schema(method="post", request_body=CreateUserSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def user_register_view(request):

    """

    View where is possible to register new Users
    Anyone can Post
    """

    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# === Get All Users ===
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users_view(request):

    """

    View where is possible to retrieve all Users
    Only allowed to Authenticated Users
    """

    queryset = User.objects.all()
    if not queryset:
        return Response("No Users found", status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# === Get/Delete User X ===
@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def user_by_id_view(request, pk):

    """

    View where is possible to Get/Delete the User which primary key is passed
    by URL
    Only allowed to Authenticated Users, but only SuperUsers can delete other Users
    """

    if request.method == "DELETE":
        user_request = request.user
        user_instance = get_object_or_404(User.objects.all(), id=pk)
        # Superuser or author can delete instance
        if user_request.is_superuser:
            user_instance.delete()
            return Response("User deleted", status=status.HTTP_200_OK)
        else:
            return Response(
                "Only superusers allowed to delete other users",
                status=status.HTTP_401_UNAUTHORIZED,
            )
    if request.method == "GET":
        user = get_object_or_404(User.objects.all(), id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# === Index Page ===
def index(request):

    """

    View that returns HTML page with a table showing the possible endpoints,
    URLS, methods allowed, parameters, return and permissions
    """

    return render(request, "index.html")
