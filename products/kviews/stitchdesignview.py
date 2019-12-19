from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..kmodels.stitchdesignmodel import StitchTypeDesign
from ..kserializers.stitchdesignserializer import StitchTypeDesignSerializer

class StitchTypeDesignViewSet(viewsets.ModelViewSet):
    queryset = StitchTypeDesign.objects.all()
    serializer_class = StitchTypeDesignSerializer

    def create(self, request, *args, **kwargs):
        if request.FILES:
            request.data['images'] = request.FILES 
        stitchdesign_serializer = StitchTypeDesignSerializer(data= request.data, context={'request': request})
        if stitchdesign_serializer.is_valid():
            stitchdesign_serializer.save()
            return Response({'stitchTypeDesignId':stitchdesign_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(stitchtype_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
