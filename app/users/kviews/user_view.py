from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
import django_filters.rest_framework
from users.models import User
from ..kserializers.user_serializer import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status 
from ..kmodels.address_model import Address
from ..kmodels.image_model import KImage
from url_filter.integrations.drf import DjangoFilterBackend
from ..paginations import LinkSetPagination
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..permissions import ActionBasedPermission

import logging
logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'retrieve','destroy'],
        AllowAny: ['list', 'create'],
    }
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['username','phone', '=email', 'is_admin', 'is_active']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id','username', 'email', 'profile', 'vendor', 'phone', 'is_admin', 'is_active']
    
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)
    
    def retrieve(self, request, *args, **kwargs):
        logger.info(" ----- User DETAIL initiated ----- ")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.debug(serializer.data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- USER CREATE initiated -----")   
        if request.data.get("_mutable"):
            request.data._mutable = True
        # User Data
        user_data = self.prepareUserData(request.data)
        user_data['created_by'] = request.auth.user_id if request.auth else None
        # Profile Data
        profileObj = request.data.get('profile')
        profile_data = self.prepareProfileData(profileObj)
        logger.debug("Data prepared. Sending data to the serializer ")
        logger.debug(user_data, profile_data)

        user_serializer = UserSerializer(data= {'user': user_data, 'profile': profile_data, 'data':request.data})
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        logger.debug({'userId':user_serializer.instance.id, "status":200})
        logger.debug("User saved successfully!!!")
        return Response({'userId':user_serializer.instance.id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- USER UPDATE initiated -----")   
        if request.data.get("_mutable"):
            request.data._mutable = True
        user_data = self.prepareUserData(request.data)
        user_data['updated_by'] = request.auth.user_id if request.auth else None
        
        profileObj = request.data.get('profile')
        profile_data = self.prepareProfileData(profileObj)

        logger.debug(profile_data, user_data)
        logger.debug("Data prepared. Sending data to the serializer ")

        serializer = self.get_serializer(self.get_object(), data= {'user': user_data, 'profile':profile_data, 'data': request.data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        logger.debug(serializer.data)
        logger.debug("Successfully USER updated")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- User DELETE initiated ----- ")
        instance = self.get_object()
        instance.is_active = False
        instance.updated_by = request.auth.user_id if request.auth else instance.updated_by
        logger.info("User deleted by userid = {} ".format(instance.updated_by))
        # PROFILE active set to false
        instance.profile.is_active = False
        instance.profile.save()
        instance.save()
        logger.debug(instance)
        logger.debug("Successfully USER DELETED")
        return Response({'success':'{} deleted successfully'.format(instance.id)}, status=status.HTTP_200_OK)

    
    #======================== CREATE USER ========================#
    def prepareUserData(self, user_info):
        user_data = {}
        if user_info:
            user_data['phone'] = user_info.get('phone')
            user_data['email'] = user_info.get('email')
            user_data['password'] = user_info.get('password')
            user_data['username'] = user_info.get('username')
            user_data['is_admin'] = user_info.get('is_admin')
        return user_data
    
    #======================== CREATE PROFILE ========================#
    def prepareProfileData(self, profile_info):
        profile_data = {}
        if profile_info:
            profile_data['firstName'] = profile_info.get('firstName')
            profile_data['lastName'] = profile_info.get('lastName')
            profile_data['userTypes'] = profile_info.get('userTypes')
            profile_data['user_role'] = profile_info.get('user_role')
            profile_data['address'] = profile_info.get('address')     
        return profile_data