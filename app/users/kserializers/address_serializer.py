from rest_framework import serializers
from ..kmodels.address_model import Address

class AddressSerializer(serializers.ModelSerializer):
    full_address = serializers.ReadOnlyField(source="get_full_address", required=False)
    class Meta:
        model = Address
        fields = ("id", "address_line_1", "address_line_2", "landmark", "postalCode","city", "state", "full_address")
        # fields = "__all__"
