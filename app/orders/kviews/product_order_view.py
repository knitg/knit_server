from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..kmodels.product_order_model import ProductOrder
from ..kserializers.product_order_serializer import ProductOrderSerializer 

import arrow
        
import logging
logger = logging.getLogger(__name__)

class ProductOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id','product_id', 'details']
    
    filter_fields = ['id','product_id', 'details']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    
    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- PRODUCT ORDER CREATE initiated -----") 
        valid_data = self.prepareProductOrderData(request.data)
        serializer = ProductOrderSerializer(data= {'data': valid_data}, context={'request': request})
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info({'productOrderId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Product Order created successfully")
        return Response({'productOrderId':serializer.instance.id}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- PRODUCT ORDER UPDATE initiated -----") 
        valid_data = self.prepareProductOrderData(request.data)
        serializer = self.get_serializer(self.get_object(), data={'data': valid_data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'productOrderId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Product order Updated successfully")
        return Response({'productOrderId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- PRODUCT ORDER DELETED initiated -----")
        instance = self.get_object()
        instance.delete()
        logger.info("Product order deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PREPARE PRODUCT OFFER DATA    
    def prepareProductOrderData(self, product_input):
        product = {}
        product['product_id'] = product_input.get('product_id')
        product['details'] = product_input.get('details')
        return product