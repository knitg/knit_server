from django.db import models
from .stitchmodel import Stitch
from .choices_model import DISCOUNT_TYPE_CHOICES

class Offers(models.Model):
    offer_title = models.CharField(null=True, max_length=80,  default=None)
    offer_code = models.CharField(null=True, max_length=80, default=None, unique=True)
    
    discount = models.CharField(null=True, max_length=120,  default=None) 
    discount_type = models.CharField(null=True, max_length=80,  choices=DISCOUNT_TYPE_CHOICES, blank=True, default='percentage')

    offer_from = models.DateTimeField(auto_now=False)
    offer_to = models.DateTimeField(auto_now=False)

    is_active = models.DateTimeField(default=False)
    # below field will tell the which category this offer belongs to
    stitch = models.ManyToManyField(Stitch)
        
    class Meta:
        db_table = 'knit_offers'
        managed = True
        verbose_name = 'Knit Offers'
    
    def __str__(self):
        return self.offer_code

