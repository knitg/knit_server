from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from ..kmodels.imagemodel import KImage
from ..kmodels.product_model import Product
from ..kserializers.product_serializer import ProductSerializer, ProductListSerializer

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend
from ..paginations import LinkSetPagination 

import logging
logger = logging.getLogger(__name__)

class ProductListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id', 'title','description', 'quantity', 'price', 'colors', 'sizes', 'offers', 'stitch', 'stitch_type']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id', 'title','description', 'quantity', 'price', 'colors', 'sizes', 'offers', 'stitch', 'stitch_type']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['id', 'title','description', 'quantity', 'price', 'colors', 'sizes', 'offers', 'stitch', 'stitch_type']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id', 'title','description', 'quantity', 'price', 'colors', 'sizes', 'offers', 'stitch', 'stitch_type']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    
    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- PRODUCT CREATE initiated -----")
        product = self.prepareProductData(request.data)
        if request.FILES:
            product.additional_data['images'] = request.FILES
        logger.debug(product)
        logger.debug("Data prepared. Sending data to the serializer ")
        product_serializer = ProductSerializer(data= {'data':request.data, 'product':product['data'], 'product_relations':product['additional_data']})
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        logger.debug({'productId':product_serializer.instance.id, "status":200})
        logger.debug("Product saved successfully!!!")
        return Response({'productId':product_serializer.instance.id}, status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        product = self.prepareProductData(request.data)
        if request.FILES:
            product.additional_data['images'] = request.FILES
        serializer = self.get_serializer(self.get_object(), data= {'data':request.data, 'product':product['data'], 'product_relations':product['additional_data']}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()
    
    #======================== CREATE PRODUCT ========================#
    def prepareProductData(self, product_input, instance=None):
        product = {}
        product['title'] = product_input.get('title')
        product['description'] = product_input.get('description')
        product['quantity'] = product_input.get('quantity')
        product['price'] = product_input.get('price')
        product['in_stock'] = product_input.get('in_stock')
        product['user'] = product_input.get('user')

        # Many to Many fields
        additional_data = {}
        additional_data['colors'] = product_input.get('colors')
        additional_data['sizes'] = product_input.get('sizes')
        additional_data['offers'] = product_input.get('offers')
        additional_data['stitch'] = product_input.get('stitch')
        additional_data['stitch_type'] = product_input.get('stitch_type')
        return {'data': product, 'additional_data': additional_data}