from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..kmodels.stitch_order_model import StitchOrder
from ..kserializers.stitch_order_serializer import StitchOrderSerializer
from django.utils.dateparse import parse_date

import arrow
        
import logging
logger = logging.getLogger(__name__)

class StitchOrderViewSet(viewsets.ModelViewSet):
    queryset = StitchOrder.objects.all()
    serializer_class = StitchOrderSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id','title', 'details', 'expected_date', 'emergency', 'stitch_id', 'is_vfm', 'material_types']
    
    filter_fields = ['id','title', 'details', 'expected_date', 'emergency', 'stitch_id', 'is_vfm', 'material_types']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    
    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- STICH ORDER CREATE initiated -----")
        valid_data = self.prepareStitchOrderData(request.data)
        serializer = StitchOrderSerializer(data= {'data': valid_data})
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info({'stitchOrderId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Stitch Order created successfully")
        return Response({'stitchOrderId':serializer.instance.id}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STICH ORDER UPDATE initiated -----") 
        valid_data = self.prepareStitchOrderData(request.data)
        serializer = self.get_serializer(self.get_object(), {'data': valid_data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'stitchOrderId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Stitch order Updated successfully")
        return Response({'stitchOrderId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STICH ORDER DELETED initiated -----")
        instance = self.get_object()
        instance.delete()
        logger.info("request master deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def prepareStitchOrderData(self, request_input):
        request_data = {}
        request_data['title'] = request_input.get('title')
        request_data['details'] = request_input.get('details')
        request_data['expected_date'] = request_input.get('expected_date')
        request_data['emergency'] = request_input.get('emergency', False)
        request_data['stitch_id'] = request_input.get('stitch_id')
        request_data['is_vfm'] = request_input.get('is_vfm', False)
        request_data['material_types'] = request_input.get('material_types')
        return request_data