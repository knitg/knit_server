import os
import csv
from django.conf import settings
from django.core.files import File
from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
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


# ## USER CAN UPLOAD STITCH FROM CSV/EXCEL
# class CSVUploadStitchViewSet(viewsets.ModelViewSet):
#     queryset = Stitch.objects.all()
#     serializer_class = StitchSerializer
     
#     parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

#     def create(self, request, *args, **kwargs):
#         logger.info(" \n\n ----- CSV STITCH CREATE initiated -----")

#         csvFile = ''
#         if request.FILES:
#             csvFile = request.FILES
#         results = []
#         for csv_file in request.FILES:
#             logger.info(" \n\n ----- CSV VENDOR CREATE initiated -----")
#             # with open(request.FILES[csv_file].name) as f:
#             decoded_file = request.FILES[csv_file].read().decode('utf-8').splitlines()
#             csv_reader = csv.DictReader(decoded_file)
#             for i, row in enumerate(csv_reader):
#                 if row:
#                     print(row)
#                     stitch_data = {}
#                     stitch_data['type'] = row.get('type')
#                     stitch_data['description'] = row.get('description') 
#                     if row.get("image"):
#                         with open(row.get('image'), 'rb') as f:
#                             stitch_data['images'] = {'images' : File(f) }                    
#                     stitch_serializer = StitchSerializer(data= stitch_data)
#                     stitch_serializer.is_valid(raise_exception=True)
#                     try:
#                         stitch_serializer.save()
#                         print("Saved Stitch")
#                         results.append({'stitchId':stitch_serializer.instance.id, "status":status.HTTP_201_CREATED})
#                     except Exception:
#                         print("Already has the Stitch")
#         return Response(results, status=status.HTTP_201_CREATED)

