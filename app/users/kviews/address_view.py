from django.shortcuts import render
from rest_framework import viewsets, generics

from ..kmodels.address_model import KAddress
from ..kserializers.address_serializer import KAddressSerializer

from url_filter.integrations.drf import DjangoFilterBackend
from ..paginations import LinkSetPagination
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser

class AddressViewSet(viewsets.ModelViewSet):
    queryset = KAddress.objects.all()
    serializer_class = KAddressSerializer
    ## Search Filter and ordering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id', 'address_line_1', 'address_line_2', 'city', 'state', 'landmark', 'postalCode']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id', 'address_line_1', 'address_line_2', 'city', 'state', 'landmark', 'postalCode']
    
    # parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited


