from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from ..kmodels.imagemodel import KImage
from ..kmodels.product_model import Product
from ..kserializers.productserializer import ProductSerializer, ProductLinkSerializer

import logging
logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- PRODUCT CREATE initiated -----")
        if request.FILES:
            request.data['images'] = request.FILES
        logger.debug(request.data)
        product_data = self.prepareProductData(request.data)
        logger.debug("Data prepared. Sending data to the serializer ")
        product_serializer = ProductSerializer(data= {'data':request.data, 'product': product_data})
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        logger.debug({'productId':product_serializer.instance.id, "status":200})
        logger.debug("Product saved successfully!!!")
        return Response({'productId':product_serializer.instance.id}, status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        if request.FILES:
            request.data['images'] = request.FILES
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
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
    def prepareProductData(self, product_input):
        product = {}
        product['title'] = product_input.get('title')
        product['description'] = product_input.get('description')
        product['quantity'] = product_input.get('quantity')
        product['price'] = product_input.get('price')
        product['in_stock'] = product_input.get('in_stock')
        product['colors'] = product_input.get('colors')
        product['sizes'] = product_input.get('sizes')
        return product

'''
        PRODUCTS BY STITCH
'''
class ProductByStitchViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductLinkSerializer

    def get_queryset(self):
        s_id = self.kwargs['stitch_id']
        return Product.objects.filter(stitch=s_id)


'''
        PRODUCTS BY STITCH TYPE
'''
class ProductByStitchTypeViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductLinkSerializer

    def get_queryset(self):
        s_id = self.kwargs['stitch_type_id']
        return Product.objects.filter(stitch_type=s_id)


'''
        PRODUCTS BY USER
'''
class ProductByUserViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductLinkSerializer

    def get_queryset(self):
        u_id = self.kwargs['user_id']
        return Product.objects.filter(user=u_id)


