from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
# from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Func, F

from users.models import User
from ..kmodels.vendor_model import Vendor
from ..kserializers.vendor_serializer import VendorSerializer
from ..kserializers.user_serializer import UserSerializer

from rest_framework.response import Response
from rest_framework import status 
from ..paginations import LinkSetPagination 

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..permissions import ActionBasedPermission
import arrow
from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

import logging
logger = logging.getLogger(__name__)

from datetime import datetime, time,date


class Sin(Func):
    function = 'SIN'

class Cos(Func):
    function = 'COS'

class Acos(Func):
    function = 'ACOS'

class Radians(Func):
    function = 'RADIANS'


class VendorUserViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'retrieve', 'destroy'],
        AllowAny: ['list', 'create']
    }
    
    search_fields = ['name','masters', 'emergency', 'doorService']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id','name', 'masters', 'closed', 'emergency', 'doorService']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    

    def get_queryset(self):
        # radius = 3
        # limit=100
        # radius = float(radius) / 1000.0
        # query = """SELECT id, (6367*acos(cos(radians(%2f))
        #         *cos(radians(17.51941353))*cos(radians(78.37865102)-radians(%2f))
        #         +sin(radians(%2f))*sin(radians(17.51941353))))
        #         AS distance FROM knit_user_profile HAVING
        #         distance < %2f ORDER BY distance LIMIT 0, %d""" % (
        #     float(17.51941353),
        #     float(78.37865102),
        #     float(17.51941353),
        #     radius,
        #     limit
        # )
        queryset = Vendor.objects.all() 
        return queryset

    def create(self, request, *args, **kwargs):

        logger.info(" \n\n ----- VENDOR CREATE initiated -----")
        #------------ PREPARE USER INFO ---------------#        
        user_info = request.data.get('user')
        profile_info = request.data.get('profile')
        user_data = self.prepareUserData(user_info, profile_info)
        if request.FILES:
            user_data['profile']['images'] = request.FILES

        #------------ PREPARE VENDOR INFO ---------------#
        vendor_details = self.prepareVendorData(request.data)
        logger.debug(user_data)
        logger.debug("Data prepared. Sending data to the serializer ")

        vendor_serializer = VendorSerializer(data= {'user': user_data, 'vendor': vendor_details, 'data': request.data}, context={'request': request})
        vendor_serializer.is_valid(raise_exception=True)
        vendor_serializer.save()
        logger.debug({'vendorId':vendor_serializer.instance.id, "status":200})
        logger.debug("Vendor saved successfully!!!")
        return Response({'vendorId':vendor_serializer.instance.id}, status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- VENDOR UPDATE initiated ----- ")
        #------------ PREPARE USER INFO ---------------#        
        user_info = request.data.get('user')
        profile_info = request.data.get('profile')
        user_data = self.prepareUserData(user_info, profile_info)
        if request.FILES:
            user_data['profile']['images'] = request.FILES

        #------------ PREPARE VENDOR INFO ---------------#
        vendor_details = self.prepareVendorData(request.data)
        
        logger.debug(vendor_details)
        logger.debug("Vendor update data prepared. Sending data to the vendor serializer ")
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
        user_data['profile'] = {}
        if user_info:
            user_data['phone'] = user_info.get('phone')
            user_data['email'] = user_info.get('email')
            user_data['password'] = user_info.get('password')
            user_data['username'] = user_info.get('username')
            
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
        vendor_details['address'] = vendor_info.get("address")
        vendor_details['userTypes'] = vendor_info.get("userTypes")
        return vendor_details

import csv

## USER CAN UPLOAD VENDORS FROM CSV/EXCEL
class UploadVendorSpreadSheetViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
     
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        csvFile = ''
        if request.FILES:
            csvFile = request.FILES

        for csv_file in request.FILES:
            logger.info(" \n\n ----- CSV VENDOR CREATE initiated -----")
            # with open(request.FILES[csv_file].name) as f:
            decoded_file = request.FILES[csv_file].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            # reader = csv_reader.reader
            results = []
            for i, row in enumerate(csv_reader):
                if (i >= 1 and row):
                    print(row)
                    user_data = {}
                    user_data['username'] = row.get('username')
                    user_data['phone'] = row.get('phone')
                    user_data['email'] = row.get('email')
                    user_data['password'] = row.get('password')
                    vendor_details = {}
                    vendor_details['name'] = row.get('name')
                    vendor_details['masters'] = 0 if row.get('masters') else 0
                    vendor_details['doorService'] = row.get('doorService')
                    vendor_details['emergency'] = row.get('emergency')


                    vendor_serializer = VendorSerializer(data= {'user': user_data, 'vendor': vendor_details, 'data': vendor_details})
                    vendor_serializer.is_valid(raise_exception=True)
                    try:
                        vendor_serializer.save()
                        print("INSIDE IF")
                        results.append({'vendorId':vendor_serializer.instance.id, "status":status.HTTP_201_CREATED})
                    except Exception:
                        print("Already has the vendor")
        return Response(results, status=status.HTTP_201_CREATED)


class VendorOnlyViewSet(viewsets.ModelViewSet): 
    serializer_class = VendorSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'retrieve', 'destroy'],
        AllowAny: ['list', 'create']
    }
    
    search_fields = ['name','masters', 'emergency', 'doorService']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id','name', 'masters', 'closed', 'emergency', 'doorService']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    

    def get_queryset(self):
        # radlat = Radians(17.43) # given latitude
        # radlong = Radians(78.37) # given longitude
        # radflat = Radians(F('address.latitude'))
        # radflong = Radians(F('address.longitude'))

        # Expression = 3959.0 * Acos(Cos(radlat) * Cos(radflat) *
        #                         Cos(radflong - radlong) +
        #                         Sin(radlat) * Sin(radflat))
         return Vendor.objects.filter(address__latitude__contains=17).filter(address__longitude__contains=78)
        # return Vendor.objects.filter(address__latitude__in=[17]).annotate(distance=Expression).order_by('distance')
 