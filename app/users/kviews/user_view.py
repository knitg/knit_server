from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from users.models import User
from ..kserializers.user_serializer import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status 
from ..kmodels.address_model import KAddress
from ..kmodels.image_model import KImage
from url_filter.integrations.drf import DjangoFilterBackend


class LinkSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ## Search Filter and ordering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['username','phone', '=email']
    
    pagination_class = LinkSetPagination

    filter_fields = ['id','username', 'email', 'profile', 'phone']
    
    # parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data= request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'userId':user_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):        
        request.data._mutable = True
        userProfile = {}
        userProfile['firstName'] = request.data.get('firstName')
        userProfile['lastName'] = request.data.get('lastName')
        userProfile['gender'] = request.data.get('gender')
        userProfile['married'] = request.data.get('married')
        userProfile['birthday'] = request.data.get('birthday')
        userProfile['anniversary'] = request.data.get('anniversary')
        userProfile['userTypes'] = request.data.get('userTypes')
        userProfile['user_role'] = request.data.get('user_role')
        userProfile['address'] = request.data.get('address')        

        serializer = self.get_serializer(self.get_object(), data= {'userProfile':userProfile, 'data': request.data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
