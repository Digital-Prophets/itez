from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from rolepermissions.roles import RolesManager
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ChangePasswordView(UpdateModelMixin, GenericViewSet):
    """
    API end point for changing password on User model.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class RoleAPIView(ViewSet):
    """
    API endpoint to list All available and roles.
    """
    def list(self, request):
        roles = RolesManager.get_roles_names()
        return Response({"roles": roles})

