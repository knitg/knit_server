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

## ALL REFERNCE TABLES DATA COLOR,SIZE, MATERIAL, CATEGORY, SUB CATEGORY
class CSVUploadProductRefTblViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- CSV CATEGORY TYPE CREATE initiated -----")
        results = []
        try:
            results.append({"colors" : create_colors()})
            results.append({"sizes" : create_sizes()})
            results.append({"materials" : create_materials()})
            
            if request.FILES.get("category"):
                results.append({"categorys" : category_csv(request.FILES.get("category"))})
            else:
                results.append({"category" : "'category' file field - Please upload csv file for category references"})
            if request.FILES.get("subcategory"):
                results.append({"sub-categorys" : sub_category_csv(request.FILES.get("subcategory"))})
            else:
                results.append({"subcategory-error" : "'subcategory' file field - Please upload csv file for sub-category references"})
        
        except FileNotFoundError as e:
            results.append({"file_error": "{}".format(e)})
            print("File not found error ??", e)
        
        except Exception as e:
            results.append({"errors": "{}".format(e)})
            print("Other error ??", e)
        return Response(results, status=status.HTTP_201_CREATED)
        
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
    logger.info(" \n\n ----- CSV COLOR CREATE initiated -----")
    results = []
    try:
        with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_colors.csv')) as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if (i >= 1 and row):
                    try:
                        color, created = ColorModel.objects.get_or_create(color=row[0])
                        if created:
                            print("REFERENCE COLORS CREATED")
                            color.save()
                        results.append({'colorId':color.id})
                    except Exception as e:
                        print("\n COLOR ERROR ", e)
                        results.append({'errors': e})

    except TypeError as e:
        logger.error("{}". format(e))
        raise TypeError("Type error {}".format(e))
        results.append({'errors': e})
    
    return results
### REFERENCE SIZES ###
def create_sizes():
    logger.info(" \n\n ----- CSV SIZE CREATE initiated -----")
    results = []
    try:
        with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_sizes.csv')) as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if (i >= 1 and row):
                    try:
                        size, created = SizeModel.objects.get_or_create(size=row[0])
                        if created:
                            print("REFERENCE SIZES CREATED")
                            size.save()
                        results.append({'sizeId':size.id})
                    except Exception as e:
                        print("\n SIZE ERROR ", e)
                        results.append({'errors': e})
                    
    except TypeError as e:
        logger.error("{}". format(e))
        raise TypeError("Type error {}".format(e))
        results.append({'errors': e})
    
    return results

### REFERENCE MATERIAL ###
def create_materials(): 
    logger.info(" \n\n ----- CSV MATERIAL CREATE initiated -----")
    results = []
    try:
        with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_materials.csv')) as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if (i >= 1 and row):
                    try:
                        material, created = MaterialModel.objects.get_or_create(material=row[0])
                        if created:
                            print("REFERENCE MATERIALS CREATED")
                            material.save()
                        results.append({'materialId':material.id})
                    except Exception as e:
                        print("\n SIZE ERROR ", e)
                        results.append({'errors': e})
                    
    except TypeError as e:
        logger.error("{}". format(e))
        raise TypeError("Type error {}".format(e))
        results.append({'errors': e})
    
    return results


#### CATEGORY CSV FILES ######
def category_csv(file):
    logger.info(" \n\n ----- CSV CATEGORY CREATE initiated -----")
    results = []
    errors = []
    try:
        # for csv_file in files:
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
    logger.info(" \n\n ----- CSV SUB CATEGORY CREATE initiated -----")
    results = []
    try:
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

