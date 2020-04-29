from django.db import models
from datetime import datetime
from django.utils.timezone import now
from .timestamp_model import TimestampedModel

class Address(TimestampedModel):
    address_type = models.CharField(default="", max_length=120)
    house_name = models.CharField(default="", max_length=120)
    address_line1= models.CharField(default='', max_length=180)
    address_line2= models.CharField(max_length=180, blank=True, null=True, default=None)
    area_name = models.CharField(default="", max_length=120)
    landmark= models.CharField(max_length=100, blank=True, null=True, default=None)
    postalCode= models.IntegerField(null=False, default=None)
    latitude= models.FloatField(max_length=20, blank=True, null=True, default=None)
    longitude= models.FloatField(max_length=20, blank=True, null=True, default=None)
    geoAddress= models.CharField(max_length=100, blank=True, null=True, default=None)
    city= models.CharField(max_length=125, null=True)
    state= models.CharField(max_length=125, blank=True, null=True, default=None)
    country= models.CharField(max_length=95, blank=True, null=True, default=None)
    
    
    def get_full_address(self):
        address_line = ""
        address_line += self.house_name if self.house_name else ""
        address_line += ", {}".format(self.address_line1) if self.address_line1 else ""
        address_line += ", {}".format(self.address_line2) if self.address_line2 else ""        
        address_line += ", {}".format(self.area_name) if self.area_name else ""
        address_line += ", {}".format(self.landmark) if self.landmark else ""
        address_line += ", {}".format(self.city) if self.city else ""
        address_line += ", {}".format(self.state) if self.state else ""
        address_line += ", {}".format(self.country) if self.country else ""
        address_line += ", {}".format(self.postalCode) if self.postalCode else ""
        return address_line


    class Meta:
        db_table = 'ref_address'
        managed = True 
    
    def __str__(self):
        return self.landmark
