from django.db import models

from .category_model import Category
from .imagemodel import KImage
from .timestamp_model import TimestampedModel
from datetime import datetime
from django.utils.timezone import now

class SubCategory(TimestampedModel):
    title = models.CharField(null=True, max_length=80,  default=None) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, default=None)
    images = models.ManyToManyField(KImage, blank=True, default=None)
    code = models.CharField(null=True, max_length=80,  default=None) 
    description = models.CharField(null=True, max_length=250,  default=None) 
    
    class Meta:
        db_table = 'ref_sub_category'
        managed = True
    
    def __str__(self):
        return self.code