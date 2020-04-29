from django.shortcuts import render
from rest_framework import viewsets, generics

from ..kmodels.address_model import Address
from ..kserializers.address_serializer import AddressSerializer

from url_filter.integrations.drf import DjangoFilterBackend
from ..paginations import LinkSetPagination
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..permissions import ActionBasedPermission

import logging
logger = logging.getLogger(__name__)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'retrieve', 'destroy'],
        AllowAny: ['list', 'create']
    }

    ## Search Filter and ordering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id', "address_type", "house_name", "address_line1", "address_line2","area_name", 'city', 'state', 'landmark', 'postalCode']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id', "address_type", "house_name", "address_line1", "address_line2","area_name", 'city', 'state', 'landmark', 'postalCode']
    
    # parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    
    def create(self, request, *args, **kwargs):
            category_serializer = AddressSerializer(data= request.data)
            try:
                category_serializer.is_valid()
                category_serializer.save()
                logger.info({'categoryId':category_serializer.instance.id, 'status':'200 Ok'})
                logger.info("Category saved successfully")
                return Response({'categoryId':category_serializer.instance.id}, status=status.HTTP_201_CREATED)
            except Exception as e:        
                logger.info(category_serializer.errors)
                logger.info("Category save failed")
                return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


