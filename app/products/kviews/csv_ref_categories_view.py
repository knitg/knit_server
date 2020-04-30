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
from ..kserializers.size_serializers import SizeSerializer
from ..kserializers.color_serializers import ColorSerilizer
from ..kserializers.material_serializers import MaterialSerilizer

from ..kmodels.color_model import ColorModel
from ..kmodels.sizes_model import SizeModel
from ..kmodels.material_model import MaterialModel

import logging
logger = logging.getLogger(__name__)
from django.db.models import Q

## USEER UPLOAD Category & SUB CATEGORY TYPES FROM CSV/EXCEL
class CSVUploadRefTblViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV CATEGORY TYPE CREATE initiated -----")
        results = []
        try:
            create_colors()
            create_sizes()
            create_materials()
            if request.FILES.get("category"):
                results.append({"categorys" : category_csv(request.FILES.get("category"))})
            if request.FILES.get("subcategory"):
                results.append({"sub-categorys" : sub_category_csv(request.FILES.get("subcategory"))})
            
        except Exception as e:
            print("something went wrong", e)
        
        # results = sub_category_csv(request.FILES)
        return Response(results, status=status.HTTP_201_CREATED)

## ONLY CATEGORY FROM CSV/EXCEL
class CSVUploadCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV CATEGORY CREATE initiated -----")
        results = []
        if request.FILES.get("category"):
            try:
                results.append(category_csv(request.FILES.get("category")))
            except Exception:
                print("somethig went wrong", e)
            
        return Response(results, status=status.HTTP_201_CREATED)

## ONLY SUB CATEGORY FROM CSV/EXCEL
class CSVUploadSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV CATEGORY TYPE CREATE initiated -----")
        results = sub_category_csv(request.FILES)
        return Response(results, status=status.HTTP_201_CREATED)


### REFERENCE COLORS ###
def create_colors():
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_colors.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                color, created = ColorModel.objects.get_or_create(color=row[0])
                if created:
                    print("REFERENCE COLORS CREATED")
                    color.save()

### REFERENCE SIZES ###
def create_sizes():
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_sizes.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                size, created = SizeModel.objects.get_or_create(size=row[0])
                if created:
                    print("REFERENCE SIZE CREATED")
                    size.save()

### REFERENCE MATERIAL ###
def create_materials(): 
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_materials.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                material, created = MaterialModel.objects.get_or_create(
                    material=row[0]
                )
                if created:
                    print("REFERENCE MATERIALS CREATED")
                    material.save()  


#### CATEGORY CSV FILES ######
def category_csv(file):
    results = []
    errors = []
    try:
        # for csv_file in files:
        logger.info(" \n\n ----- CSV CATEGORY CREATE initiated -----")
        decoded_file = file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(decoded_file)
        for i, row in enumerate(csv_reader):
            if row:
                logger.info(" \n\n")
                logger.info(row)
                category_data = {}
                category_data['title' ] = row.get('title' )                    
                desc = row.get('description').encode('ascii','ignore') if row.get('description') else None
                category_data['description'] = desc.decode("utf-8")[:100] if desc else None
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
                    results.append({'categoryId':category_serializer.instance.id})
                except Exception as e:
                    logger.error("Something wrong with CATEGORY serializer save")
                    print("Already has the CATEGORY", e)
                    results.append({'error': "{}".format(e)})
        
    except AttributeError as e:
        logger.error("Attribute Error {} \n".format(e))
        results.append({'attribute_error': "{}".format(e), "status":status.HTTP_400_BAD_REQUEST})
    except UnicodeDecodeError as e:
        logger.error("UnicodeDecodeError: file.read().decode('utf-8') here {}".format(e))
        results.append({'unicode_error': "{}".format(e), "status":status.HTTP_400_BAD_REQUEST})
    return results
    

#### CATEGORY TYPE CSV FILES ######
def sub_category_csv(file):
    try:
        results = []
        decoded_file = file.read().decode(errors='replace').splitlines()
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
                desc = row.get('description').encode('ascii','ignore') if row.get('description') else None
                category_data['description'] = desc.decode("utf-8")[:200] if desc else None
                if row.get("image"):
                    with open(row.get('image'), 'rb') as f:
                        category_data['images'] = {'images' : File(f) }
                        logger.info(category_data['images'])

                logger.info("PREPARED CATEGORY DATA ", category_data)                    
                subcategory_serializer = SubCategorySerializer(data= category_data)
                
                try:
                    logger.info(subcategory_serializer.is_valid())       
                    subcategory_serializer.is_valid(raise_exception=True)
                    logger.info("Before serializer save call")
                    subcategory_serializer.save()
                    logger.info({'subCategoryId':subcategory_serializer.instance.id, 'status':'200 Ok'})
                    print("SAVED SUB CATEGORY")
                    results.append({'subCategoryId':subcategory_serializer.instance.id})
                except Exception as e:
                    logger.error("Something wrong with SUB CATEGORY serializer save")
                    print("Already has the SUB CATEGORY", e)
                    results.append({'error': "{}".format(e)})

    except AttributeError as e:
        logger.error("Attribute Error {} \n".format(e))
        results.append({'attribute_error': "{}".format(e), "status":status.HTTP_400_BAD_REQUEST})
    except UnicodeDecodeError as e:
        logger.error("UnicodeDecodeError: file.read().decode('utf-8') here {}".format(e))
        results.append({'unicode_error': "{}".format(e), "status":status.HTTP_400_BAD_REQUEST})
    return results

