from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from ..models import *
from ..serializers import ParkingSerializer


# Create your views here.
class ListParking(generics.ListCreateAPIView):
    queryset = ParkingImport.objects.all()
    serializer_class = ParkingSerializer


class DetailParking(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParkingImport.objects.all()
    serializer_class = ParkingSerializer
