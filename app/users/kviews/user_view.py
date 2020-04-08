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
from ..kmodels.address_model import KAddress
from ..kmodels.image_model import KImage
from url_filter.integrations.drf import DjangoFilterBackend
from ..paginations import LinkSetPagination



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ## Search Filter and ordering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['username','phone', '=email', 'is_admin', 'is_active']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id','username', 'email', 'profile', 'phone', 'is_admin', 'is_active']
    
    # parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited


    def create(self, request, *args, **kwargs):        
        # User Data
        user_data = self.prepareUserData(request.data)
        # Profile Data
        profileObj = request.data.get('profile')
        profile_data = self.prepareProfileData(profileObj)
        
        user_serializer = UserSerializer(data= {'user': user_data, 'profile': profile_data, 'data':request.data})
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'userId':user_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):   
        request.data._mutable = True     
        
        user_data = self.prepareUserData(request.data)
        
        profileObj = request.data.get('profile')
        profile_data = self.prepareProfileData(profileObj)      

        serializer = self.get_serializer(self.get_object(), data= {'user': user_data, 'profile':profile_data, 'data': request.data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        # instance.delete()
        return Response({'success':'{} deleted successfully'.format(instance.id)}, status=status.HTTP_200_OK)

    
    #======================== CREATE USER ========================#
    def prepareUserData(self, user_info):
        user_data = {}
        if user_info:
            user_data['phone'] = user_info.get('phone')
            user_data['email'] = user_info.get('email')
            user_data['password'] = user_info.get('password')
            user_data['username'] = user_info.get('username')
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