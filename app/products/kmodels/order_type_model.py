from django.db import models
from .imagemodel import KImage

from datetime import datetime
from django.utils.timezone import now
from .timestamp_model import TimestampedModel

# order type is what type of order user will make?
class OrderType(models.Model):
    type = models.CharField(null=True, max_length=80,  default=None)
    code = models.CharField(null=True, max_length=80,  default=None)
    images = models.ManyToManyField(KImage, blank=True, default=None)
    description = models.CharField(null=True, max_length=80,  default=None)

    class Meta:
        db_table = 'ref_order_type'
        managed = True
    
    def __str__(self):
        return self.code

    
    def save(self, *args, **kwargs):
        if not self.type:
            raise ValueError("Please enter Order type")
        else:
            replaced_txt = re.sub(r'\W+', '_', self.type)
            self.code = replaced_txt.upper()

        super(OrderType).save(*args, **kwargs)


