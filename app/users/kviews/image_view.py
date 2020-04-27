from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser

from ..kmodels.image_model import KImage
from ..kserializers.image_serializer import KImageSerializer

from rest_framework.response import Response
from rest_framework import status 

class ImageViewSet(viewsets.ModelViewSet):
    # parser_class = (FileUploadParser,)
    queryset = KImage.objects.all()
    serializer_class = KImageSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        images_arr = []
        for image in request.FILES:
            image_serializer = KImageSerializer(data= {'description': request.data.get('description'), 'image': request.FILES[image]})
            if image_serializer.is_valid():
                image_serializer.save()
                images_arr.append(image_serializer.instance.id)
                return Response({'image_ids': images_arr}, status=status.HTTP_201_CREATED)
            else:
                return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)









