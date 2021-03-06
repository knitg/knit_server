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
    
    def get_queryset(self):
        radius = 5
        limit=100
        radius = float(radius) / 1000.0
        query = """SELECT
                        id, (
                        3959 * acos (
                        cos ( radians(17) )
                        * cos( radians( latitude ) )
                        * cos( radians( longitude ) - radians(78) )
                        + sin ( radians(17) )
                        * sin( radians( latitude ) )
                        )
                    ) AS distance
                    FROM ref_address
                    HAVING distance > 1 
                    ORDER BY `distance`  DESC LIMIT 0 , 100"""
        queryset = Address.objects.raw(query) 
        return queryset
    
    def create(self, request, *args, **kwargs):
        address_serializer = AddressSerializer(data= request.data)
        try:
            address_serializer.is_valid()
            address_serializer.save()
            logger.info({'categoryId':address_serializer.instance.id, 'status':'200 Ok'})
            logger.info("Category saved successfully")
            return Response({'categoryId':address_serializer.instance.id}, status=status.HTTP_201_CREATED)
        except Exception as e:        
            logger.info(address_serializer.errors)
            logger.info("Category save failed")
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


