from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..kmodels.stitchmodel import Stitch
from ..kserializers.stitchserializer import StitchSerializer

import logging
logger = logging.getLogger(__name__)

class StitchViewSet(viewsets.ModelViewSet):
    queryset = Stitch.objects.all()
    serializer_class = StitchSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['type','description', 'code']
    
    filter_fields = ['type','description', 'code']
    
    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- STITCH CREATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))

        stitch_serializer = StitchSerializer(data= request.data)
        if stitch_serializer.is_valid():
            stitch_serializer.save()
            logger.info({'stitchId':stitch_serializer.instance.id, 'status':'200 Ok'})
            logger.info("Stitch saved successfully")
            return Response({'stitchId':stitch_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            logger.info(stitch_serializer.errors)
            logger.info("Stitch save failed")
            return Response(stitch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH UPDATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))     
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'stitchId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Stitch Updated successfully")
        return Response({'stitchId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("Stitch deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("Stitch Image deleted {}".format(e.id))