from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser

from users.models import User
from ..kmodels.vendor_model import KVendorUser
from ..kserializers.vendor_serializer import KVendorUserSerializer

from rest_framework.response import Response
from rest_framework import status 
 

class VendorUserViewSet(viewsets.ModelViewSet):
    queryset = KVendorUser.objects.all()
    serializer_class = KVendorUserSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        # set to mutable
        request.data._mutable = True
        ## Files assigned to request data images
        request.data['images'] = []
        user_data = {}
        user_data['phone'] = request.data.get('phone') if request.data.get('phone') else None
        user_data['email'] = request.data.get('email') if request.data.get('email') else None
        user_data['password'] = request.data.get('password') if request.data.get('password') else None
        user_data['user_role'] = request.data.get('user_role') if request.data.get('user_role') else None
        user_data['username'] = request.data.get('username') if request.data.get('username') else None
        if request.FILES:
             request.data['images'] = request.FILES

        vendor_details = {}
        
        vendor_details['name'] = request.data.get('name') if request.data.get('name') else None
        vendor_details['open_time'] = request.data.get('open_time') if request.data.get('open_time') else None
        vendor_details['close_time'] = request.data.get('close_time') if request.data.get('close_time') else None
        vendor_details['masters_count'] = request.data.get('masters_count') if request.data.get('masters_count') else None
        vendor_details['is_weekends'] = request.data.get('is_weekends') if request.data.get('is_weekends') else False
        vendor_details['alternate_days'] = request.data.get('alternate_days') if request.data.get('alternate_days') else None
        vendor_details['is_open'] = request.data.get('is_open') if request.data.get('is_open') else True
        vendor_details['is_door_service'] = request.data.get('is_door_service') if request.data.get('is_door_service') else False
        vendor_details['is_emergency_available'] = request.data.get('is_emergency_available') if request.data.get('is_emergency_available') else True
        vendor_details['address'] = request.data.get('address') if request.data.get('address') else None
        
        vendor_serializer = KVendorUserSerializer(data= {'user': user_data, 'vendor': vendor_details, 'data': request.data}, context={'request': request})
        
        ### Vendor serializer save initiated
        if vendor_serializer.is_valid():
            vendor_serializer.save()
            return Response({'vendorId':vendor_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.FILES:
            request.data['images'] = request.FILES
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
