from rest_framework import serializers
from ..kmodels.color_model import ColorModel

class ColorChoiceSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ('id', 'color')
