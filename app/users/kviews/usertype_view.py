from django.shortcuts import render
from rest_framework import viewsets, generics

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..permissions import ActionBasedPermission

from ..kmodels.usertype_model import UserType
from ..kserializers.usertype_serializer import UserTypeSerializer

from rest_framework.response import Response
from rest_framework import status 

import logging
logger = logging.getLogger(__name__)

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

    # permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: [ 'create', 'update', 'partial_update', 'destroy'],
        AllowAny: ['list', 'retrieve'],
    }

    def create(self, request, *args, **kwargs):
        logger.info(" \n\n ----- USER TYPE CREATE initiated -----")   
        # User Data
        user_serializer = UserTypeSerializer(data= request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        logger.debug({'userTypeId':user_serializer.instance, "status":200})
        logger.debug("User type saved successfully!!!")
        return Response({'userId':user_serializer.instance.id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- USER TYPE UPDATE initiated -----")
        serializer = self.get_serializer(self.get_object(), data= request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({'userId':serializer.data.id}, status=status.HTTP_201_CREATED)




