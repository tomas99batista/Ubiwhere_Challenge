from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Occurence
from .serializers import OccurenceSerializer 

# TODO: Finalizar API
# TODO: Auth (jwt auth)
# TODO: Docker
# TODO: Documentação
# TODO: Página dos endpoints
# TODO: README.md: Como fazer deploy e correr, etc
# TODO: Postman collection

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

    # GET -> Search/Filter
    # TODO: Filter by distance
    # TODO: Filter by author
    def get(self, request):
        queryset = Occurence.objects.all()

        # Filter by category
        category = self.request.query_params.get('category', None)
        queryset = queryset.filter(category=category) if category is not None else queryset

        # Filter by distance
        # point = self.request.query_params.get('point', None)
        # queryset = queryset.filter(category=category) if category is not None else queryset

        # Filter by author
        # user = self.request.query_params.get('user', None)
        # queryset = queryset.filter(user=user) if user is not None else queryset

        serializer = OccurenceSerializer(queryset, many=True)
        return Response(serializer.data) 