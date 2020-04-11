from django.shortcuts import render
from rest_framework import viewsets, generics

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..permissions import ActionBasedPermission

from ..kmodels.usertype_model import UserType
from ..kserializers.usertype_serializer import UserTypeSerializer

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: [ 'create', 'update', 'partial_update', 'destroy'],
        AllowAny: ['list', 'retrieve'],
    }
