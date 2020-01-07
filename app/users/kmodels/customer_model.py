from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.conf import settings
from .address_model import KAddress
from users.models import User

class KCustomer(models.Model):
    name= models.CharField(null=True, max_length=80,  default=None)  
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False)
    address = models.ForeignKey(KAddress, on_delete=models.CASCADE, default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

    class Meta:
        db_table = 'knit_customer'
        managed = True
        verbose_name = 'Knit Customer'
        verbose_name_plural = 'Knit Customers'
    
    def __str__(self):
        return self.name

