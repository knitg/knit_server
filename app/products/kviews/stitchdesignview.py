from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kserializers.stitchdesignserializer import StitchTypeDesignSerializer

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

import logging
logger = logging.getLogger(__name__)

class StitchTypeDesignViewSet(viewsets.ModelViewSet):
    queryset = StitchTypeDesign.objects.all()
    serializer_class = StitchTypeDesignSerializer
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['type','description', 'code', 'stitchType']
    
    filter_fields = ['type','description', 'code', 'stitchType']
    
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH TYPE DESIGN CREATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES 
            logger.info("Images length = {}".format(len(request.FILES)))
        stitchdesign_serializer = StitchTypeDesignSerializer(data= request.data)
        stitchdesign_serializer.is_valid(raise_exception=True)
        stitchdesign_serializer.save()
        logger.info({'stitchTypeId':stitchdesign_serializer.instance.id, 'status':'200 Ok'})
        logger.info("STITCH TYPE DESIGN saved successfully")
        return Response({'stitchTypeId':stitchdesign_serializer.instance.id}, status=status.HTTP_201_CREATED)

        
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH TYPE DESIGN UPDATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES        
            logger.info("Images length = {}".format(len(request.FILES))) 
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'stitchId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Stitch Updated successfully")
        return Response(serializer.data)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- STITCH TYPE DESIGN DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("STITCH TYPE DESIGN deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("Image deleted {}".format(e.id))

