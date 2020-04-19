from django.db import models

from datetime import datetime
from django.utils.timezone import now
from .timestamp_model import TimestampedModel

class RequestMaster(TimestampedModel):

    # Product details
    duration = models.IntegerField(null=True, max_length=80,  default=None) # hours
    details = models.CharField(null=True, max_length=180,  default=None)
    master_id = models.IntegerField(null=True, blank=True, default=None)

    # VFM is for sent notification to all the masters so master can opt the facility
    is_vfm = models.BooleanField(null=True, blank=True, default=False)

    from_date = models.DateField(auto_now_add=False,null=True,blank=True)
    to_date = models.DateField(auto_now_add=False,null=True,blank=True)
    
    class Meta:
        db_table = 'knit_order_master'
        managed = True
    
    def __str__(self):
        return self.title

