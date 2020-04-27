from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser

from users.models import User
from ..kmodels.vendor_model import Vendor
from ..kserializers.vendor_serializer import VendorSerializer
from ..kserializers.user_serializer import UserSerializer

from rest_framework.response import Response
from rest_framework import status 
from ..paginations import LinkSetPagination 

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..permissions import ActionBasedPermission

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

import logging
logger = logging.getLogger(__name__)

from datetime import datetime, time,date

class RefUploadExcelViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
