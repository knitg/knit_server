from django.db import models

from datetime import datetime
from django.utils.timezone import now
from .image_model import OrderImage
from .timestamp_model import TimestampedModel

class StitchOrder(TimestampedModel):

    # Product basic info
    title = models.CharField(null=True, max_length=180,  default=None)
    details = models.CharField(null=True, max_length=180,  default=None)
    expected_date =  models.DateTimeField(auto_now=False, blank=True, null=True)
    emergency =  models.BooleanField(default=True, blank=True, null=True)
    
    category_id= models.IntegerField(null=True, default=None) # CATEGORY
    
    # expected should something look like 1,2,3,4 (material ids)
    material_types =  models.CharField(null=True, max_length=180,  default=None) # material ids separated with commas
    
    is_vfm = models.BooleanField(default=True, blank=True, null=True)

    images = models.ManyToManyField(OrderImage, blank=True, default=None)
    
    class Meta:
        db_table = 'knit_order_stich'
        managed = True
    
    def __str__(self):
        return self.title

