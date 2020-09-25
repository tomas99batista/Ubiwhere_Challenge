from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
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


# POST: Add Occurrence
@api_view(["POST"])
def add_new_occurrence(request):
    user = request.user
    serializer = OccurrenceCreationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PATCH: Update given Occurrence |
# DELETE: Delete given occurrence |
# GET: Retrieve given Occurrence by ID
@api_view(["PATCH", "DELETE", "GET"])
def update_delete_get_occurrence(request, pk):
    if request.method == "PATCH":
        user = request.user
        if not user.is_superuser:
            return Response(
                "Only superusers are allowed to update occurrences",
                status=status.HTTP_400_BAD_REQUEST,
            )
        occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=pk)
        serializer = OccurrencePatchSerializer(
            occurrence, data=request.data, partial=True
        )  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        user = request.user
        occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=pk)
        # Superuser or author can delete instance
        if occurrence.author == user or user.is_superuser:
            occurrence.delete()
            return Response("Occurrence deleted", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                "Only superusers or creators allowed to delete occurrences",
                status=status.HTTP_400_BAD_REQUEST,
            )

    if request.method == "GET":
        occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=pk)
        print(occurrence)
        serializer = OccurrenceSerializer(occurrence)
        return Response(serializer.data)


# GET: Filter occurrence by author/category/distance to given point
@api_view(["GET"])
def filter_occurrences(request):
    queryset = Occurrence.objects.all()

    # Filter by category
    category = request.query_params.get("category", None)
    queryset = queryset.filter(category=category) if category is not None else queryset

    # Filter by author
    username = request.query_params.get("username", None)
    queryset = (
        queryset.filter(author__username=username) if username is not None else queryset
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
        point = GEOSGeometry(
            "POINT(" + str(longitude) + " " + str(latitude) + ")", srid=4326
        )
        for occurrence in queryset:
            # Calculate the distance from the stored point to the given point
            distance = occurrence.geographic_location.distance(point)
            # If the distance from the given point to the stored point is bigger than the distance passed, exclude that point
            queryset = (
                queryset.exclude(occurrence_id=occurrence.occurrence_id)
                if distance > float(distance_range)
                else queryset
            )

    # If no type of filter (category, distance or author) is passed.
    if (not category and not latitude and not longitude and not distance_range and not username):
        return Response(
            "BAD REQUEST: You need to pass at least one type of filter.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not queryset:
        return Response(
            "No data found for the given filters", status=status.HTTP_204_NO_CONTENT
        )

    serializer = OccurrenceSerializer(queryset, many=True)
    return Response(serializer.data)


# GET: Get all occurrences
@api_view(["GET"])
def get_all_occurrences(request):
    queryset = Occurrence.objects.all()
    serializer = OccurrenceSerializer(queryset, many=True)
    return Response(serializer.data)


# POST: Register a new user
@api_view(["POST"])
def user_register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET: Returns all users
@api_view(["GET"])
def retrieve_all_users(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


# GET: Get user by ID |
# DELETE: Delete given User (by ID) - only allowed by superusers
@api_view(["GET", "DELETE"])
def get_delete_user(request, pk):
    if request.method == "DELETE":
        user_request = request.user
        user_instance = get_object_or_404(User.objects.all(), id=pk)
        # Superuser or author can delete instance
        if user_request.is_superuser:
            user_instance.delete()
            return Response("User deleted", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                "Only superusers allowed to delete other users",
                status=status.HTTP_400_BAD_REQUEST,
            )

    if request.method == "GET":
        user = get_object_or_404(User.objects.all(), id=pk)
        print(user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


def index(request):
    params = {}
    return render(request, "index.html", params)
