from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.stitchmodel import Stitch
from ..kserializers.stitchserializer import StitchSerializer


class StitchViewSet(viewsets.ModelViewSet):
    queryset = Stitch.objects.all()
    serializer_class = StitchSerializer
    
    def create(self, request, *args, **kwargs):
        if request.FILES:
            request.data['images'] = request.FILES

        stitch_serializer = StitchSerializer(data= request.data)
        if stitch_serializer.is_valid():
            stitch_serializer.save()
            return Response({'stitchId':stitch_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(stitch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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