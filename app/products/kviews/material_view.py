from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser, JSONParser
from rest_framework import viewsets

from ..kmodels.material_model import MaterialModel
from ..kserializers.material_serializers import MaterialSerilizer
 

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = MaterialModel.objects.all()
    serializer_class = MaterialSerilizer

    parser_classes = (JSONParser, FormParser, MultiPartParser, FileUploadParser)