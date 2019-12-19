from django.db import models
from datetime import datetime
from django.utils.timezone import now

class KAddress(models.Model):
    address_line_1= models.CharField(default='', max_length=50)
    address_line_2= models.CharField(max_length=50, blank=True, null=True, default=None)
    landmark= models.CharField(max_length=50, blank=True, null=True, default=None)
    postalCode= models.IntegerField(null=False, default=None)
    latitude= models.FloatField(max_length=20, blank=True, null=True, default=None)
    longitude= models.FloatField(max_length=20, blank=True, null=True, default=None)
    geoAddress= models.CharField(max_length=100, blank=True, null=True, default=None)
    city= models.CharField(max_length=25, null=True)
    state= models.CharField(max_length=25, blank=True, null=True, default=None)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        db_table = 'knit_address'
        managed = True
        verbose_name = 'Knit Address'
        verbose_name_plural = 'Knit Addresses'
    
    def __str__(self):
        return self.landmark
