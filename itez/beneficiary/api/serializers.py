from rest_framework import serializers
from itez.beneficiary.models import (
    Province,
    District,
    ServiceArea,
    WorkDetail
)

class ProvinceSerializer(serializers.ModelSerializer):
    """
    Province Serializer
    """
    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    """
    District Serializer
    """
    class Meta:
        model = District
        fields = '__all__'


class ServiceAreaSerializer(serializers.ModelSerializer):
    """
    Service Area Serializer
    """
    class Meta:
        model = ServiceArea
        fields = '__all__'



class WorkDetailSerializer(serializers.ModelSerializer):
    """
    Work Detail Serializer
    """
    class Meta:
        model = WorkDetail
        fields = '__all__'
        

