from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from ..kmodels.imagemodel import KImage
from ..kmodels.product_model import Product
from ..kserializers.product_serializer import ProductSerializer, ProductLinkSerializer

import logging
logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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

        # Many to Many fields
        additional_data = {}
        additional_data['colors'] = product_input.get('colors')
        additional_data['sizes'] = product_input.get('sizes')
        additional_data['offers'] = product_input.get('offers')
        additional_data['stitch'] = product_input.get('stitch')
        additional_data['stitch_type'] = product_input.get('stitch_type')
        additional_data['stitch_type_design'] = product_input.get('stitch_type_design')
        return {'data': product, 'additional_data': additional_data}

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


