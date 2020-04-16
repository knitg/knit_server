from django.shortcuts import render 
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework import filters
from url_filter.integrations.drf import DjangoFilterBackend

from ..kmodels.prices_model import Prices
from ..kmodels.offers_model import Offers
from ..kserializers.price_serializer import PriceSerializer
from ..kserializers.offers_serializer import OfferSerializer

import logging
logger = logging.getLogger(__name__)

class PricesViewSet(viewsets.ModelViewSet):
    queryset = Offers.objects.all()
    serializer_class = PriceSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['price','actual_price','product','offers']
    
    filter_fields = ['price','actual_price','product','offers']
    
    def create(self, request, *args, **kwargs):  
        logger.info(" \n\n ----- PRICE CREATE initiated -----")
        price_serializer = PriceSerializer(data= request.data)
        price_serializer.is_valid(raise_exception=True)
        price_serializer.save()
        logger.info({'priceId':price_serializer.instance.id, 'status':'200 Ok'})
        logger.info("Price saved successfully")
        return Response({'priceId':price_serializer.instance.id}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        logger.info(" \n\n ----- PRICE UPDATE initiated -----")
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info({'priceId':serializer.instance.id, 'status':'200 Ok'})
        logger.info("Price Updated successfully")
        return Response({'priceId':serializer.instance.id}, status=status.HTTP_200_OK)
 
    def destroy(self, request, *args, **kwargs):
        logger.info(" \n\n ----- Price DELETED initiated -----")
        instance = self.get_object()
        instance.delete()
        logger.info("Price deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)