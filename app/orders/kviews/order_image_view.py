from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser

from ..kmodels.image_model import OrderImage
from ..kserializers.image_serializer import OrderImageSerializer

from rest_framework.response import Response
from rest_framework import status 

class OrderImageViewSet(viewsets.ModelViewSet):
    # parser_class = (FileUploadParser,)
    queryset = OrderImage.objects.all()
    serializer_class = OrderImageSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        images_arr = []
        for image in request.FILES:
            image_serializer = OrderImageSerializer(data= {'description': request.data['description'], 'image': request.FILES[image]})
            if image_serializer.is_valid():
                image_serializer.save()
                images_arr.append(image_serializer.instance.id)
                return Response({'image_ids': images_arr}, status=status.HTTP_201_CREATED)
            else:
                return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)









