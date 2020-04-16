from rest_framework import serializers
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser

from ..kmodels.offers_model import Offers

class OfferSerializer(serializers.ModelSerializer):
    discount_type = serializers.SerializerMethodField()
    errors = {}
    def get_discount_type(self, obj):
        return obj.get_discount_type_display()

    class Meta:
        model = Offers
        fields = ('id','offer_title','offer_code','discount','discount_type','offer_from','offer_to', 'stitch')
        parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited
        
    def validate(self, data):
        self.errors = {}
        if data.get('offer_code'):
            data['offer_code'] = data.get('offer_code', '').replace(" ", "_").upper()
        else:
            self.errors['required'] = 'Offer code is required'
        if data.get('offer_title'):
            data['offer_title'] = data.get('offer_code')
        else:
            self.errors['required'] = 'Offer Title is required'
        if data.get('offer_from'):
            data['offer_from'] = data.get('offer_from')
        else:
            self.errors['required'] = 'Offer start date is required'
        if data.get('offer_to'):
            data['offer_to'] = data.get('offer_to')
        else:
            self.errors['required'] = 'Offer end date is required'
        raise serializers.ValidationError(self.errors)        
        return data

    def create(self, validated_data):
        ## Image data 
        validated_data['code'] = validated_data.get('code')
        offer = Offers.objects.create(**validated_data)
        offer.save()
        return offer

    def update(self, instance, validated_data):
        # Update the Foo instance
        instance.offer_title = validated_data.get('offer_title', instance.offer_title)
        instance.offer_code = validated_data.get('offer_code', instance.offer_code).upper()
        instance.discount = validated_data.get('discount', instance.discount)
        instance.discount_type = validated_data.get('discount_type', instance.discount_type)
        instance.offer_from = validated_data.get('offer_from', instance.offer_from)
        instance.offer_to = validated_data.get('offer_to', instance.offer_to)
        instance.stitch = validated_data.get('stitch', instance.stitch)
        instance.save()

        return instance 