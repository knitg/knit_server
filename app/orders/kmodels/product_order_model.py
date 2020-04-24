from django.db import models

from datetime import datetime
from django.utils.timezone import now
from .image_model import OrderImage
from .timestamp_model import TimestampedModel

class ProductOrder(TimestampedModel):

    product_id= models.IntegerField(null=True, default=None)
    details = models.CharField(null=True, max_length=180,  default=None)
    
    class Meta:
        db_table = 'knit_order_product'
        managed = True
    
    def __str__(self):
        return self.title

