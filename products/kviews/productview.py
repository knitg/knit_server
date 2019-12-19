from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.imagemodel import KImage
from ..kmodels.productmodel import Product
from ..kserializers.productserializer import ProductSerializer, ProductLinkSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        if request.FILES:
            request.data['images'] = request.FILES 

        product_serializer = ProductSerializer(data= request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({'productId':product_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
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


