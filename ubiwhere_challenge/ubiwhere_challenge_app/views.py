from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_gis.filters import DistanceToPointFilter
from django.contrib.gis.geos import GEOSGeometry

from .models import Occurence
from .serializers import OccurenceSerializer

# TODO: Finalizar API
# TODO: Auth (jwt auth)
# TODO: Página dos endpoints
# TODO: Postman collection
# TODO: Documentação código
# TODO: README.md: Como fazer deploy e correr, etc

def index(request):
    params = {}
    return render(request, 'index.html', params)

# --- API VIEWS ---
class OccurenceView(APIView):
    # POST -> Creation
    # TODO: Qdo inserir state ou dar erro ou então passa-lo para normal
    # TODO: User info
    def post(self, request):
        serializer = OccurenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT -> Update
    # TODO: Apenas deixar dar update no state
    # TODO: User info
    def put(self, request):
        occurence = get_object_or_404(Occurence.objects.all(), occurence_id=self.request.data.get('occurence_id'))
        serializer = OccurenceSerializer(occurence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET -> Search/Filter´
    # Possible filter:
        # By category
        # By author
        # By distance, passing latitude, longitude and a range Z, in km
    # TODO: Filter by distance
    # TODO: Filter by author
    def get(self, request):
        queryset = Occurence.objects.all()
        # Filter by category
        category = self.request.query_params.get('category', None)
        queryset = queryset.filter(category=category) if category is not None else queryset

        # Filter by author
        # user = self.request.query_params.get('user', None)
        # queryset = queryset.filter(user=user) if user is not None else queryset

        # Filter by distance (in m)
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        distance_range = self.request.query_params.get('range', None)  
        # If the 3 arguments to the distance filter are passed
        if latitude or longitude or distance_range:
            # If not all 3 (latitude, longitude and distance) distance filters are passed.
            # an bad request error is generated
            if not latitude and not longitude and not distance_range:
                return Response("BAD REQUEST: Distance filter needs a latitude, a longitude and a distance range.", status=status.HTTP_400_BAD_REQUEST)            
            # Create a point from the given longitude and latitude
            point = GEOSGeometry('POINT(' + str(longitude) + ' ' + str(latitude) + ')', srid=4326)
            for occurence in queryset:
                # Calculate the distance from the stored point to the given point
                distance=occurence.geographic_location.distance(point)
                # If the distance from the given point to the stored point is bigger than the distance passed, exclude that point
                queryset = queryset.exclude(occurence_id=occurence.occurence_id) if distance > float(distance_range) else queryset

        # If no type of filter (category, distance or author) is passed.
        if not category and not latitude and not longitude and not distance_range: #and not user
            return Response("BAD REQUEST: You need to pass at least one type of filter.", status=status.HTTP_400_BAD_REQUEST)                   

        serializer = OccurenceSerializer(queryset, many=True)
        return Response(serializer.data) 
