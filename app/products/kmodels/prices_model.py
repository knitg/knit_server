from django.db import models
from .offers_model import Offers
from .choices_model import CURRENCY_CHOICES

class Prices(models.Model):
    price= models.FloatField(null=True, max_length=80,  default=None)
    actual_price= models.FloatField(max_length=80, null=False, blank=True, default=None)
    discounted_price= models.FloatField(max_length=80, null=False, blank=True, default=None)
    
    currency_type= models.CharField(null=True, max_length=80,  choices=CURRENCY_CHOICES, blank=True, default='R')
    offers = models.ManyToManyField(Offers)

    class Meta:
        db_table = 'knit_prices'
    
    def __str__(self):
        return self.price

