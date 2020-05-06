from rest_framework import serializers
from ..kmodels.address_model import Address

class AddressSerializer(serializers.ModelSerializer):
    full_address = serializers.ReadOnlyField(source="get_full_address", required=False)
    errors = {}
    class Meta:
        model = Address
        fields = ("id", "address_type", "house_name", "address_line1", "address_line2", "latitude", "longitude", "area_name", "landmark", "postalCode","city", "state", "full_address")
        # fields = "__all__"
    
    def validate(self, data):
        self.errors = {}
        if data.get('house_name') is None:
            self.errors['house_name'] = "House/Apartment name is required"
        address_instance = Address.objects.filter(house_name__icontains = data.get('house_name'))
        if len(address_instance):
            self.errors['exists'] = "This address already exists"
        if data.get('address_type') is None:
            self.errors['address_type'] = "Address type is required"
        if len(self.errors):
            raise serializers.ValidationError(self.errors)
        return data