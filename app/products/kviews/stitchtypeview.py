from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.stitchtypemodel import StitchType
from ..kserializers.stitchtypeserializer import StitchTypeSerializer, StitchTypeByStitchSerializer

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

import logging
logger = logging.getLogger(__name__)

class StitchTypeViewSet(viewsets.ModelViewSet):
    queryset = StitchType.objects.all()
    serializer_class = StitchTypeSerializer
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['type','description', 'code', 'stitch']
    
    filter_fields = ['type','description', 'code', 'stitch']
    
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)
    
    
    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH TYPE CREATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES 
            logger.info("Images length = {}".format(len(request.FILES)))

        stitchtype_serializer = StitchTypeSerializer(data= request.data)
        if stitchtype_serializer.is_valid():
            stitchtype_serializer.save()
            logger.info({'stitchTypeId':stitchtype_serializer.instance.id, 'status':'200 Ok'})
            logger.info("Stitch Type saved successfully")
            return Response({'stitchTypeId':stitchtype_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            logger.info(stitchtype_serializer.errors)
            logger.info("StitchType save failed")
            return Response(stitchtype_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH TYPE UPDATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))        
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'stitchId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Stitch Updated successfully")
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH TYPE DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("Stitch Type deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("Stitch Image deleted {}".format(e.id))
