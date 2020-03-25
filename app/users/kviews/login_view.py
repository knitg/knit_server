from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from django.contrib.auth import authenticate
from users.models import User
from ..kserializers.user_serializer import UserSerializer

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse


from rest_framework.response import Response
from rest_framework import status 
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request):
        pwd = False
        email = request.data.get("email")
        phone = request.data.get("phone")
        username = request.data.get("username")
        password = request.data.get("password")

        if (password is None):
            return Response({'error': 'Please provide valid email/phone and password'}, status=HTTP_400_BAD_REQUEST)
        password_valid = User.check_password(password, "pbkdf2_sha256")
        # if password is None:
        #     return Response({'error': 'Please provide valid email/phone and password'}, status=HTTP_400_BAD_REQUEST)
        # user = authenticate(username=username)
        if email is not None:
            user = User.objects.filter(email=email, password=password).values()
        elif phone is not None:
            user = User.objects.filter(phone=phone, password=password).values()
        else:
            user = User.objects.filter(username=username, password=password).values()
            # user = authenticate(username=username, password=password)
 
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
        
        return JsonResponse(list(user), status=HTTP_200_OK, safe=False)






