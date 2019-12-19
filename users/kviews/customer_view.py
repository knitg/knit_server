from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser

from ..kmodels.user_model import User
from ..kmodels.customer_model import KCustomer
from ..kserializers.customer_serializer import KCustomerSerializer

from rest_framework.response import Response
from rest_framework import status 
 

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = KCustomer.objects.all()
    serializer_class = KCustomerSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser) # set parsers if not set in settings. Edited

    def create(self, request, *args, **kwargs):
        # set to mutable
        request.data._mutable = True
        ## Files assigned to request data images
        request.data['images'] = []
        user_data = {}
        user_data['phone'] = request.data.get('phone') if request.data.get('phone') else None
        user_data['email'] = request.data.get('email') if request.data.get('email') else None
        user_data['password'] = request.data.get('password') if request.data.get('password') else None
        user_data['user_role'] = request.data.get('user_role') if request.data.get('user_role') else None
        user_data['userName'] = request.data.get('userName') if request.data.get('userName') else None
        if request.FILES:
             request.data['images'] = request.FILES

        customer_details = {}
        
        customer_details['name'] = request.data.get('name') if request.data.get('name') else None
        customer_details['address'] = request.data.get('address') if request.data.get('address') else None
        
        customer_serializer = KCustomerSerializer(data= {'user': user_data, 'customer': customer_details, 'data': request.data}, context={'request': request})
        
        ### Vendor serializer save initiated
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response({'customerId':customer_serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.FILES:
            request.data['images'] = request.FILES
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for e in instance.images.all():
            instance.images.remove(e)
            KImage.objects.get(id=e.id).delete()







