from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from itez.beneficiary.models import (
Province,
District,
ServiceArea,
WorkDetail
)

from itez.beneficiary.api.serializers import (
    ProvinceSerializer,
    DistrictSerializer,
    ServiceAreaSerializer,
    WorkDetailSerializer
)


class ProvinceList(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
    ):
    """
    API end point for Province model list, create and update.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DistrictList(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet
    ):
    """
    API end point for District model list, create and update.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)