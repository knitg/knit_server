from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.imagemodel import KImage
from ..kserializers.imageserializer import KImageSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = KImage.objects.all()
    serializer_class = KImageSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    
    def create(self, request, *args, **kwargs):
        images_arr = []
        for image in request.FILES:
            image_serializer = KImageSerializer(data= {'description': request.data['description'], 'image': request.FILES[image]})
            if image_serializer.is_valid():
                image_serializer.save()
                images_arr.append(image_serializer.instance.id)
                return Response({'image_ids': images_arr}, status=status.HTTP_201_CREATED)
            else:
                return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
