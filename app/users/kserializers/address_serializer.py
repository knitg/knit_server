from rest_framework import serializers
from ..kmodels.address_model import Address

class AddressSerializer(serializers.ModelSerializer):
    full_address = serializers.ReadOnlyField(source="get_full_address", required=False)
    
    class Meta:
        model = Address
        fields = ("id", "address_type", "house_name", "address_line1", "address_line2","area_name", "landmark", "postalCode","city", "state", "full_address")
        # fields = "__all__"
    
    def validate(self, data):
        if data.get('address_type') is None:
            data['address_type'] = data.get('title', '').replace(" ", "_").upper()
        else:
            raise serializers.ValidationError("Address type is required")
        return data