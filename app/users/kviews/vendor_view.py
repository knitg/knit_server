from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser

from users.models import User
from ..kmodels.vendor_model import KVendorUser
from ..kserializers.vendor_serializer import KVendorUserSerializer
from ..kserializers.user_serializer import UserSerializer

from rest_framework.response import Response
from rest_framework import status 
from ..paginations import LinkSetPagination 

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

class VendorUserViewSet(viewsets.ModelViewSet):
    queryset = KVendorUser.objects.all()
    serializer_class = KVendorUserSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['name','masters', 'emergency', 'doorService']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id','name', 'masters', 'closed', 'emergency', 'doorService']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    
    def create(self, request, *args, **kwargs):

        #------------ PREPARE USER INFO ---------------#        
        user_info = request.data.get('user')
        profile_info = request.data.get('profile')
        user_data = self.prepareUserData(user_info, profile_info)
        if request.FILES:
            user_data['profile']['images'] = request.FILES

        #------------ PREPARE VENDOR INFO ---------------#
        vendor_details = self.prepareVendorData(request.data)

        vendor_serializer = KVendorUserSerializer(data= {'user': user_data, 'vendor': vendor_details, 'data': request.data}, context={'request': request})
        if vendor_serializer.is_valid():
            vendor_serializer.save()
            return Response({'vendorId':vendor_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        #------------ PREPARE USER INFO ---------------#        
        user_info = request.data.get('user')
        profile_info = request.data.get('profile')
        user_data = self.prepareUserData(user_info, profile_info)
        if request.FILES:
            user_data['profile']['images'] = request.FILES

        #------------ PREPARE VENDOR INFO ---------------#
        vendor_details = self.prepareVendorData(request.data)
        
        serializer = self.get_serializer(self.get_object(), data={'user': user_data, 'vendor': vendor_details, 'data': request.data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'id':serializer.data.get("id")}, status=status.HTTP_202_ACCEPTED)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        if instance.user:
            # instance.images.remove(e)
            User.objects.get(id=instance.user.id).delete()
    
    
    #======================== CREATE USER ========================#
    def prepareUserData(self, user_info, profile_info):
        user_data = {}
        if user_info:
            user_data['phone'] = user_info.get('phone')
            user_data['email'] = user_info.get('email')
            user_data['password'] = user_info.get('password')
            user_data['username'] = user_info.get('username')
            user_data['profile'] = {}
            if profile_info:
                user_data['profile']['firstName'] = profile_info.get('firstName')
                user_data['profile']['lastName'] = profile_info.get('lastName')
                user_data['profile']['userTypes'] = profile_info.get('userTypes')
                user_data['profile']['user_role'] = profile_info.get('user_role')
                user_data['profile']['address'] = profile_info.get('address')     
        return user_data
  
    #======================== CREATE VENDOR ========================#
    def prepareVendorData(self, vendor_info):
        vendor_details = {}
        vendor_details['name'] = vendor_info.get('name')
        vendor_details['openTime'] = vendor_info.get('openTime')
        vendor_details['closeTime'] = vendor_info.get('closeTime')
        vendor_details['masters'] = vendor_info.get('masters')
        vendor_details['isWeekends'] = vendor_info.get('isWeekends')
        vendor_details['alternateDays'] = vendor_info.get('alternateDays')
        vendor_details['closed'] = vendor_info.get('closed')
        vendor_details['doorService'] = vendor_info.get('doorService')
        vendor_details['emergency'] = vendor_info.get('emergency')
        return vendor_details
