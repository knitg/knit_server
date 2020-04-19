from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..kmodels.offers_model import Offers
from ..kserializers.offers_serializer import OfferSerializer
from django.utils.dateparse import parse_date

import arrow
        
import logging
logger = logging.getLogger(__name__)

class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offers.objects.all()
    serializer_class = OfferSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['title','code','discount','from_date','to_date', 'is_active']
    
    filter_fields = ['title','code','discount','from_date','to_date', 'is_active']
    
    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- OFFER CREATE initiated -----")
        offer_serializer = OfferSerializer(data= {'data': request.data})
        
        offer_serializer.is_valid(raise_exception=True)
        offer_serializer.save()
        logger.info({'offerId':offer_serializer.instance.id, 'status':'200 Ok'})
        logger.info("Offer saved successfully")
        return Response({'offerId':offer_serializer.instance.id}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- OFFER UPDATE initiated -----") 
        serializer = self.get_serializer(self.get_object(), data={'data': request.data}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'offerId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Offer Updated successfully")
        return Response({'offerId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- OFFER DELETED initiated -----")
        instance = self.get_object()
        instance.delete()
        logger.info("offer deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)