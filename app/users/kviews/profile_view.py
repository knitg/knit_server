from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.exceptions import APIException

from ..kmodels.profile_model import Profile
from ..kserializers.profile_serializer import ProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..renderers import DataJSONRenderer
from ..paginations import LinkSetPagination

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..permissions import ActionBasedPermission

import logging
logger = logging.getLogger(__name__)

class ProfileListViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['firstName','lastName', 'gender', 'user', 'birthday', 'anniversary'], 
    
    pagination_class = LinkSetPagination

    filter_fields = ['firstName','lastName', 'gender', 'user', 'birthday', 'anniversary']
    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited


    def get_queryset(self):
        profile = Profile.objects.filter(is_active=True)
        return profile
 
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        profile = Profile.objects.select_related('user').filter(user__pk=self.kwargs['user_id'], is_active=True)
        return profile

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        filter[self.lookup_field] = self.kwargs['user_id']
        return get_object_or_404(queryset, **filter)

    def update(self, request, *args, **kwargs):
        logger.info(" ----- PROFILE UPDATE initiated ----- ")
        if request.FILES:
            request.data['images'] = request.FILES
        
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        logger.debug(serializer.data)
        logger.debug("Profile updated successfully")
        return Response(serializer.data)

class ProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested profile does not exist.'