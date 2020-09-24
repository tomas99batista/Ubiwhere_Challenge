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
    OccurrencePatchSerializer
)
from .models import Occurrence

# Add new Occurrence
@api_view(['POST'])
def add_new_occurrence(request):
    user = request.user
    serializer = OccurrenceCreationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update an occurrence
@api_view(['PATCH'])
def update_occurrence(request, pk):
    user = request.user
    if not user.is_superuser:
        return Response("Only superusers allowed", status=status.HTTP_400_BAD_REQUEST)
    occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=pk)
    serializer = OccurrencePatchSerializer(occurrence, data=request.data, partial=True) # set partial=True to update a data partially
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Filter occurences
@api_view(['GET'])
def filter_occurences(request):
    queryset = Occurrence.objects.all()

    # Filter by category
    category = request.query_params.get('category', None)
    queryset = queryset.filter(category=category) if category is not None else queryset

    # Filter by author
    username = request.query_params.get('username', None)
    queryset = queryset.filter(author__username=username) if username is not None else queryset

    # Filter by distance (in m)
    latitude = request.query_params.get('latitude', None)
    longitude = request.query_params.get('longitude', None)
    distance_range = request.query_params.get('range', None)  
    # If the 3 arguments to the distance filter are passed
    if latitude or longitude or distance_range:
        # If not all 3 (latitude, longitude and distance) distance filters are passed.
        # an bad request error is generated
        if not latitude and not longitude and not distance_range:
            return Response("BAD REQUEST: Distance filter needs a latitude, a longitude and a distance range.", status=status.HTTP_400_BAD_REQUEST)            
        # Create a point from the given longitude and latitude
        point = GEOSGeometry('POINT(' + str(longitude) + ' ' + str(latitude) + ')', srid=4326)
        for occurrence in queryset:
            # Calculate the distance from the stored point to the given point
            distance=occurrence.geographic_location.distance(point)
            # If the distance from the given point to the stored point is bigger than the distance passed, exclude that point
            queryset = queryset.exclude(occurrence_id=occurrence.occurrence_id) if distance > float(distance_range) else queryset

    # If no type of filter (category, distance or author) is passed.
    if not category and not latitude and not longitude and not distance_range and not username:
        return Response("BAD REQUEST: You need to pass at least one type of filter.", status=status.HTTP_400_BAD_REQUEST)                   

    serializer = OccurrenceSerializer(queryset, many=True)
    return Response(serializer.data) 

# Retrieve all occurrences
@api_view(['GET'])
def get_all_occurrences(request):
    queryset = Occurrence.objects.all()
    serializer = OccurrenceSerializer(queryset, many=True)
    return Response(serializer.data)

# Register User
@api_view(['POST'])
def user_register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve All Users
@api_view(['GET'])
def retrieve_all_users(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


#class OccurrenceView(APIView):
#    # POST -> Creation
#    # TODO: Qdo inserir state ou dar erro ou então passa-lo para normal
#    def post(self, request):
#        # Needs to be authenticated to create a new occurrence as he will be the author
#        permission_classes = (IsAuthenticated,)
#        serializer = OccurrenceSerializer(data=request.data, author=request.user)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    # PUT -> Update
#    # TODO: Apenas deixar dar update no state
#    def put(self, request):
#        # Needs to be the owner in order to change the occurrence
#        permission_classes = (IsOwner,)
#        occurrence = get_object_or_404(Occurrence.objects.all(), occurrence_id=self.request.data.get('occurrence_id'))
#        serializer = OccurrenceSerializer(occurrence, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    # GET -> Search/Filter
#    # Possible filter (combined):
#        # By category
#        # By author
#        # By distance, passing X latitude, Y longitude and a range Z, in meters
#    # TODO: Filter by author
#    def get(self, request):



def index(request):
    params = {}
    return render(request, 'index.html', params)
