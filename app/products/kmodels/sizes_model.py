from django.db import models

SIZE_CHOICES = (
        ('xs', 'Xtra Small'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'Xtra Large'),
        ('xxl', 'Double XL'),
        ('xxxl', 'Triple XL'),
        )

class SizeModel(models.Model):
    size= models.CharField(null=True, max_length=80,  choices=SIZE_CHOICES, blank=True, default=None)
    class Meta:
        db_table = 'ref_sizes'
    
    def __str__(self):
        return "{}, {}".format(self.size)
