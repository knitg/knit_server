from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser

from users.models import User
from ..kserializers.user_serializer import UserSerializer
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status 
from ..kmodels.address_model import KAddress
from ..kmodels.image_model import KImage

class UserListViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

class UserDetailViewSet(viewsets.ViewSet):
    
    def list(self, request):
        pass

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class UserRegisterViewSet(viewsets.ViewSet):
    
    def create(self, request, *args, **kwargs):
        images_arr = []
        if request.FILES:
            request.data['images'] = request.FILES

        user_serializer = UserSerializer(data= request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'userId':user_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginViewSet(viewsets.ViewSet):
    
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

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
        
        userProfile['firstName'] = request.data.get('firstName') if request.data.get('firstName') else None
        userProfile['lastName'] = request.data.get('lastName') if request.data.get('lastName') else None
        userProfile['gender'] = request.data.get('gender') if request.data.get('gender') else None
        userProfile['married'] = request.data.get('married') if request.data.get('married') else None
        userProfile['birthday'] = request.data.get('birthday') if request.data.get('birthday') else False
        userProfile['anniversary'] = request.data.get('anniversary') if request.data.get('anniversary') else None
        userProfile['userTypes'] = request.data.get('userTypes') if request.data.get('userTypes') else True
        userProfile['user_role'] = request.data.get('user_role') if request.data.get('user_role') else False
        userProfile['address'] = request.data.get('address') if request.data.get('address') else True        

        serializer = self.get_serializer(self.get_object(), data= {'userProfile':userProfile, 'data': request.data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
