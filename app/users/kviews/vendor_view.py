from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser

from users.models import User
from ..kmodels.vendor_model import KVendorUser
from ..kserializers.vendor_serializer import KVendorUserSerializer
from ..kserializers.user_serializer import UserSerializer

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
        user_data['username'] = request.data.get('username') if request.data.get('username') else None
        if request.FILES:
             request.data['images'] = request.FILES
        
        vendor_details = {}
        
        vendor_details['name'] = request.data.get('name') if request.data.get('name') else None
        vendor_details['openTime'] = request.data.get('openTime') if request.data.get('openTime') else None
        vendor_details['closeTime'] = request.data.get('closeTime') if request.data.get('closeTime') else None
        vendor_details['masters'] = request.data.get('masters') if request.data.get('masters') else None
        vendor_details['isWeekends'] = request.data.get('isWeekends') if request.data.get('isWeekends') else False
        vendor_details['alternateDays'] = request.data.get('alternateDays') if request.data.get('alternateDays') else None
        vendor_details['closed'] = request.data.get('closed') if request.data.get('closed') else True
        vendor_details['doorService'] = request.data.get('doorService') if request.data.get('doorService') else False
        vendor_details['emergency'] = request.data.get('emergency') if request.data.get('emergency') else True
        
        profile_details = {}
        
        profile_details['userTypes'] = request.data.get('userTypes') if request.data.get('userTypes') else None
        profile_details['address'] = request.data.get('address') if request.data.get('address') else None
        if request.FILES:
             profile_details['images'] = request.FILES
        
        vendor_serializer = KVendorUserSerializer(data= {'user': user_data, 'vendor': vendor_details, 'profile':profile_details, 'data': request.data}, context={'request': request})
        
        ### Vendor serializer save initiated
        if vendor_serializer.is_valid():
            vendor_serializer.save()
            return Response({'vendorId':vendor_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # set to mutable
        request.data._mutable = True
        
        if request.FILES:
            request.data['images'] = request.FILES
        # request.data['name'] = request.data.get('name') if request.data.get('openTime') else instance.name   
        # request.data['openTime'] = request.data.get('openTime') if request.data.get('openTime') else instance.openTime
        # request.data['closeTime'] = request.data.get('closeTime') if request.data.get('closeTime') else  instance.closeTime
        # request.data['masters'] = request.data.get('masters') if request.data.get('masters') else  instance.masters
        # request.data['isWeekends'] = request.data.get('isWeekends') if request.data.get('isWeekends') else instance.isWeekends
        # request.data['alternateDays'] = request.data.get('alternateDays') if request.data.get('alternateDays') else instance.alternateDays
        # request.data['closed'] = request.data.get('closed') if request.data.get('closed') else instance.closed
        # request.data['doorService'] = request.data.get('doorService') if request.data.get('doorService') else instance.doorService
        # request.data['emergency'] = request.data.get('emergency') if request.data.get('emergency') else instance.emergency
        user = UserSerializer(request.data)
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
        if instance.user:
            # instance.images.remove(e)
            User.objects.get(id=instance.user.id).delete()