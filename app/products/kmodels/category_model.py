from django.db import models
from .imagemodel import KImage

from datetime import datetime
from django.utils.timezone import now
from .timestamp_model import TimestampedModel

class Category(TimestampedModel):
    title = models.CharField(null=True, max_length=80,  default=None)    
    code = models.CharField(null=True, max_length=80,  default=None)
    images = models.ManyToManyField(KImage, blank=True, default=None)
    description = models.CharField(null=True, max_length=80,  default=None)

    class Meta:
        db_table = 'ref_category'
        managed = True
    
    def __str__(self):
        return self.code


