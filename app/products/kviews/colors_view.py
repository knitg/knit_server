from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets

from ..kmodels.color_model import ColorModel
from ..kserializers.color_serializers import ColorSerilizer
 

class ColorsViewSet(viewsets.ModelViewSet):
    queryset = ColorModel.objects.all()
    serializer_class = ColorSerilizer

    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)