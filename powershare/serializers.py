from rest_framework.serializers import ModelSerializer

from powershare.models import PowerShareStation, PowerShareOrder


class PowerShareStationSerializer(ModelSerializer):
    class Meta:
        model = PowerShareStation
        fields = '__all__'


class PowerShareOrderSerializer(ModelSerializer):
    class Meta:
        model = PowerShareOrder
        fields = ('pickupStation','returnTime')
