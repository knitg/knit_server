from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..kmodels.request_masters_model import RequestMaster
from ..kserializers.request_master_serializer import RequestMasterSerializer
from django.utils.dateparse import parse_date

import arrow
        
import logging
logger = logging.getLogger(__name__)

class RequestMasterViewSet(viewsets.ModelViewSet):
    queryset = RequestMaster.objects.all()
    serializer_class = RequestMasterSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id','duration', 'details', 'from_date', 'to_date', 'master_id', 'is_vfm']
    
    filter_fields = ['id','duration', 'details', 'from_date', 'to_date', 'master_id', 'is_vfm']
    
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- REQUEST MASTER CREATE initiated -----") 
        valid_data = self.prepareRequestMasterData(request.data)
        serializer = RequestMasterSerializer(data= {'data': valid_data})
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info({'requestMasterId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Request Master successfully")
        return Response({'requestMasterId':serializer.instance.id}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- REQUEST MASTER UPDATE initiated -----") 
        valid_data = self.prepareRequestMasterData(request.data)
        serializer = self.get_serializer(self.get_object(), data={'data': valid_data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'requestMasterId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("REQUEST Master Updated successfully")
        return Response({'requestMasterId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- REQUEST MASTER DELETED initiated -----")
        instance = self.get_object()
        instance.delete()
        logger.info("request master deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def prepareRequestMasterData(self, request_input):
        request_data = {}
        request_data['duration'] = request_input.get('duration')
        request_data['details'] = request_input.get('details')
        request_data['from_date'] = request_input.get('from_date')
        request_data['to_date'] = request_input.get('to_date')
        request_data['master_id'] = request_input.get('master_id')
        request_data['is_vfm'] = request_input.get('is_vfm')
        return request_data