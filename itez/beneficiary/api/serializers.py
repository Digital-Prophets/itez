from rest_framework import fields, serializers
from itez.beneficiary.models import (
    Beneficiary,
    BeneficiaryParent,
    Province,
    District,
    ServiceArea,
    WorkDetail
)


class BeneficiarySerializer(serializers.ModelSerializer):
    """
    Beneficiary serializer.
    """
    class Meta:
        model = Beneficiary
        fields = '__all__'


class BeneficiaryParentSerializer(serializers.ModelSerializer):
    """
    BeneficiaryParent serializer.
    """
    class Meta:
        model = BeneficiaryParent
        fields = '__all__'


class ProvinceModelSerializer(serializers.ModelSerializer):
    """
    Province Serializer.
    """
    class Meta:
        model = Province
        fields = '__all__'


class DistrictModelSerializer(serializers.ModelSerializer):
    """
    District Serializer.
    """
    class Meta:
        model = District
        fields = '__all__'


class ServiceAreaModelSerializer(serializers.ModelSerializer):
    """
    Service Area Serializer.
    """
    class Meta:
        model = ServiceArea
        fields = '__all__'



class WorkDetailModelSerializer(serializers.ModelSerializer):
    """
    Work Detail Serializer.
    """
    class Meta:
        model = WorkDetail
        fields = '__all__'
        

