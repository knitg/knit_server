import os
import csv
from django.conf import settings
from django.core.files import File

from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.category_model import Category
from ..kmodels.sub_category_model import SubCategory
from ..kserializers.category_serializer import CategorySerializer
from ..kserializers.sub_category_serializer import SubCategorySerializer

import logging
logger = logging.getLogger(__name__)
from django.db.models import Q

## USER CAN UPLOAD CATEGORY FROM CSV/EXCEL
class CSVUploadCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV CATEGORY CREATE initiated -----")
        results = []
        results = category_csv(request.FILES)
        return Response(results, status=status.HTTP_201_CREATED)

## USER CAN UPLOAD SUB CATEGORY TYPES FROM CSV/EXCEL
class CSVUploadSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV CATEGORY TYPE CREATE initiated -----")
        results = sub_category_csv(request.FILES)
        return Response(results, status=status.HTTP_201_CREATED)

#### CATEGORY CSV FILES ######
def category_csv(files):
    try:    
        results = []
        for csv_file in files:
            logger.info(" \n\n ----- CSV CATEGORY CREATE initiated -----")
            decoded_file = files[csv_file].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for i, row in enumerate(csv_reader):
                if row:
                    logger.info(" \n\n")
                    logger.info(row)
                    category_data = {}
                    category_data['title' ] = row.get('title' )                    
                    desc = row.get('description').encode('ascii','ignore')
                    category_data['description'] = desc.decode("utf-8")[:100]
                    if row.get("image"):
                        with open(row.get('image'), 'rb') as f:
                            category_data['images'] = {'images' : File(f) }
                            logger.info(category_data['images'])
                    
                    logger.info("PREPARED CATEGORY DATA ", category_data)                    
                    category_serializer = CategorySerializer(data= category_data)
                    try:
                        logger.info(category_serializer.is_valid())       
                        category_serializer.is_valid(raise_exception=True)
                        logger.info("Before serializer save call")
                        category_serializer.save()
                        logger.info({'categoryId':category_serializer.instance.id, 'status':'200 Ok'})
                        print("SAVED CATEGORY")
                        results.append({'categoryId':category_serializer.instance.id, "status":status.HTTP_201_CREATED})
                    except Exception:
                        logger.error("Something wrong with CATEGORY serializer save")
                        print("Already has the CATEGORY")
        return results
    except Exception as e:
        print("Something went wrong", e)

#### CATEGORY TYPE CSV FILES ######
def sub_category_csv(files):
    try:
        results = []
        for csv_file in files:
            decoded_file = files[csv_file].read().decode(errors='replace').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for i, row in enumerate(csv_reader):
                if row:
                    logger.info(" \n\n")
                    logger.info(row)
                    print(row)
                    category_data = {}
                    category_data['title' ] = row.get('title' )
                    category_obj = Category.objects.filter(code__icontains=row.get("category-code"))
                    logger.info("---- SUB CATEGORY OBJ --- ")
                    logger.info(category_obj)
                    if len(category_obj):
                        category_data['category'] = category_obj[0].id
                    desc = row.get('description').encode('ascii','ignore')
                    category_data['description'] = desc.decode("utf-8")[:200]
                    if row.get("image"):
                        with open(row.get('image'), 'rb') as f:
                            category_data['images'] = {'images' : File(f) }
                            logger.info(category_data['images'])

                    logger.info("PREPARED CATEGORY DATA ", category_data)                    
                    subcategory_serializer = SubCategorySerializer(data= category_data)
                    logger.info(subcategory_serializer.is_valid())
                    subcategory_serializer.is_valid(raise_exception=True)
                    try:
                        logger.info("Before serializer save call")
                        subcategory_serializer.save()
                        logger.info({'subCategoryId':subcategory_serializer.instance.id, 'status':'200 Ok'})
                        print("SAVED SUB CATEGORY")
                        results.append({'subCategoryId':subcategory_serializer.instance.id, "status":status.HTTP_201_CREATED})
                    except Exception:
                        logger.error("Something wrong with sub category serializer save")
                        print("Already has the SUB CATEGORY")
        return results
    except Exception as e:
        print("Something went wrong", e)
