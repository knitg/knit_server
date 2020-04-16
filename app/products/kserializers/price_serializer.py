from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser

from ..kmodels.prices_model import Prices
from .offers_serializer import OfferSerializer


class PriceSerializer(serializers.ModelSerializer):
    offers = serializers.SerializerMethodField()
    errors = {}

    def get_offers(self, obj):
        serializer = OfferSerializer(obj.offers, many=True)
        return serializer.data 

    class Meta:
        model = Prices
        fields = ('id','price','actual_price', 'offers')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
        
    def validate(self, data):
        self.errors = {}
        if data.get('price'):
            data['price'] = data.get('price', 0.00)
        else:
            self.errors['required'] = 'Price is required'

        raise serializers.ValidationError(self.errors)        
        return data

    def create(self, validated_data):
        offers = validated_data.pop("offers")
        prices = Prices.objects.create(**validated_data)
        if offers is not None:
            if isinstance(offers, list):
                offer = list(UserType.objects.filter(id__in=offers))
                prices.offers.set(offer)
            else:
                raise serializers.ValidationError("Offers expected an array")
        prices.save()
        return prices

    def update(self, instance, validated_data):
        errors = []
        # Update the Foo instance
        instance.offer_title = validated_data.get('price', instance.offer_title)
        instance.offer_code = validated_data.get('actual_price', instance.offer_code).upper()
        instance.discount = validated_data.get('discounted_price', instance.discount)
        instance.discount_type = validated_data.get('currency_type', instance.discount_type)
        instance.offer_from = validated_data.get('product', instance.offer_from)
        if self.initial_data.get('offers') is not None:
            if isinstance(self.initial_data.get('offers'), list):
                offer = list(UserType.objects.filter(id__in=self.initial_data.get("offers")))
                instance.offers.set(offer)
            else:
                raise serializers.ValidationError("Offers expected an array")
        instance.save() 
        return instance 