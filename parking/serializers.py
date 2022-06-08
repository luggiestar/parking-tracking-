from rest_framework import serializers

from .models import ParkingImport


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingImport
        fields = '__all__'
