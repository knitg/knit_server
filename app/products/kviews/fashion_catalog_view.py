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
from ..kmodels.fashion_catalog_model import FashionCatalog
from ..kserializers.category_serializer import CategorySerializer
from ..kserializers.fashion_catalog_serializer import FashionCatalogSerializer

import logging
logger = logging.getLogger(__name__)

class FashionCatalogViewSet(viewsets.ModelViewSet):
    queryset = FashionCatalog.objects.all()
    serializer_class = FashionCatalogSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id','title', 'userId', 'images', 'category','customizable', 'details']
    
    filter_fields = ['id','title', 'userId', 'images', 'category','customizable', 'details']
    
    def create(self, request, *args, **kwargs):   
        logger.info(" \n\n ----- FASHION CATALOG CREATE initiated -----")
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

        fashion_catalog_serializer = FashionCatalogSerializer(data= {'data':request.data, 'catalog':catalog, 'catalog_relations':relations})
        if fashion_catalog_serializer.is_valid():
            fashion_catalog_serializer.save()
            logger.info({'catalogId':fashion_catalog_serializer.instance.id, 'status':'200 Ok'})
            logger.info("Fashion Catalog saved successfully")
            return Response({'catalogId':fashion_catalog_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            logger.info(fashion_catalog_serializer.errors)
            logger.info("Fashion Catalog save failed")
            return Response(fashion_catalog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Fashion Catalog UPDATE initiated -----")
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

        serializer = self.get_serializer(self.get_object(), data={'data':request.data, 'catalog':catalog, 'catalog_relations':relations}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'catalogId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Fashion Catalog  Updated successfully")
        return Response({'catalogId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Fashion Catalog DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("Fashion Catalog deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("Category Image deleted {}".format(e.id))
