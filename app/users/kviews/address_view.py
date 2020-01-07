from django.shortcuts import render
from rest_framework import viewsets, generics

from ..kmodels.address_model import KAddress
from ..kserializers.address_serializer import KAddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = KAddress.objects.all()
    serializer_class = KAddressSerializer

