from django.shortcuts import render, get_object_or_404
import datetime
from rest_framework import generics
from django.http import JsonResponse, HttpResponse
from ..models import *
from ..serializers import ParkingSerializer


# Create your views here.
class ListParking(generics.ListCreateAPIView):
    queryset = ParkingImport.objects.all()
    serializer_class = ParkingSerializer


class DetailParking(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParkingImport.objects.all()
    serializer_class = ParkingSerializer


def parking_import_entrace(request):
    today = datetime.datetime.now()
    entrace = ParkingTracking.objects.filter(activity__event = 'ENTRANCE').count()
    print(today)
    print(entrace)
    return HttpResponse(str(entrace))

def parking_import_parking(request):
    today = datetime.datetime.now()
    entrace = ParkingTracking.objects.filter(activity__event = 'PARKING').count()
    print(today)
    print(entrace)
    return HttpResponse(str(entrace))

