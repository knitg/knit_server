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

from ..kmodels.category_model import Category
from ..kmodels.maggam_catalog_model import MaggamCatalog
from ..kserializers.category_serializer import CategorySerializer
from ..kserializers.maggam_catalog_serializer import MaggamCatalogSerializer

import logging
logger = logging.getLogger(__name__)

class MaggamCatalogViewSet(viewsets.ModelViewSet):
    queryset = MaggamCatalog.objects.all()
    serializer_class = MaggamCatalogSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id','title', 'userId', 'images', 'category','customizable', 'details']
    
    filter_fields = ['id','title', 'userId', 'images', 'category','customizable', 'details']
    
    def create(self, request, *args, **kwargs):   
        logger.info(" \n\n ----- MAGGAM CATALOG CREATE initiated -----")
        relations = {}
        if request.FILES:
            relations['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))
        relations['category'] = request.data.get("category")
        catalog = {}
        catalog['title'] = request.data.get("title")
        catalog['userId'] = request.data.get("userId")
        catalog['details'] = request.data.get("details")
        catalog['customizable'] = request.data.get("customizable")

        maggam_catalog_serializer = MaggamCatalogSerializer(data= {'data':request.data, 'catalog':catalog, 'catalog_relations':relations})
        if maggam_catalog_serializer.is_valid():
            maggam_catalog_serializer.save()
            logger.info({'catalogId':maggam_catalog_serializer.instance.id, 'status':'200 Ok'})
            logger.info("Maggam Catalog saved successfully")
            return Response({'catalogId':maggam_catalog_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            logger.info(maggam_catalog_serializer.errors)
            logger.info("Maggam Catalog save failed")
            return Response(maggam_catalog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Maggam Catalog UPDATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))     
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'catalogId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Maggam Catalog  Updated successfully")
        return Response({'catalogId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Maggam Catalog DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("Maggam Catalog deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("Category Image deleted {}".format(e.id))


# ## USER CAN UPLOAD CATEGORY FROM CSV/EXCEL
# class CSVUploadCategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
     
#     parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

#     def create(self, request, *args, **kwargs):
#         logger.info(" \n\n ----- CSV CATEGORY CREATE initiated -----")

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
#                     stitch_data['title'] = row.get('title')
#                     stitch_data['description'] = row.get('description') 
#                     if row.get("image"):
#                         with open(row.get('image'), 'rb') as f:
#                             stitch_data['images'] = {'images' : File(f) }                    
#                     category_serializer = CategorySerializer(data= stitch_data)
#                     category_serializer.is_valid(raise_exception=True)
#                     try:
#                         category_serializer.save()
#                         print("Saved Category")
#                         results.append({'categoryId':category_serializer.instance.id, "status":status.HTTP_201_CREATED})
#                     except Exception:
#                         print("Already has the Category")
#         return Response(results, status=status.HTTP_201_CREATED)

