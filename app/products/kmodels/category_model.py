from django.db import models
from .imagemodel import KImage
import re
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
    

    def save(self, *args, **kwargs):
        if not self.title:
            raise ValueError("Please enter Category title")
        else:
            replaced_txt = re.sub(r'\W+', '_', self.title)
            self.code = replaced_txt.upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


