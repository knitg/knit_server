from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.sub_category_model import SubCategory
from ..kserializers.sub_category_serializer import SubCategorySerializer

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

import logging
logger = logging.getLogger(__name__)

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['title','description', 'code', 'category']
    
    filter_fields = ['title','description', 'code', 'category']
    
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)
    
    
    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- SUB CATEGORY  CREATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES 
            logger.info("Images length = {}".format(len(request.FILES)))

        subcategory_serializer = SubCategorySerializer(data= request.data)
        try:
            subcategory_serializer.is_valid()
            subcategory_serializer.save()
            logger.info({'subCategoryId':subcategory_serializer.instance.id, 'status':'200 Ok'})
            logger.info("SubCategory Type saved successfully")
            return Response({'subCategoryId':subcategory_serializer.instance.id}, status=status.HTTP_201_CREATED)
        except AssertionError as e:
            logger.info(subcategory_serializer.errors)
            logger.info("SubCategory save failed")
            return Response(subcategory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            logger.info("KEY ERROR", e)
            print("KEY ERROR")
        except ValueError as e:
            logger.info("Value ERROR", e)

    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- SUB CATEGORY  UPDATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
            logger.info("Images length = {}".format(len(request.FILES)))        
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'subCategoryId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("SubCategory Updated successfully")
        return Response({'subCategoryId':serializer.data}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- SUB CATEGORY  DELETED initiated -----")
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        logger.info("SubCategory Type deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
            logger.info("SubCategory Image deleted {}".format(e.id))
