from django.shortcuts import render
from rest_framework import viewsets, generics

from ..kmodels.usertype_model import KUserType
from ..kserializers.usertype_serializer import KUserTypeSerializer

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = KUserType.objects.all()
    serializer_class = KUserTypeSerializer





