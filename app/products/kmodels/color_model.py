from django.db import models

COLOR_CHOICES = (
        ('white', 'White'),
        ('black', 'Black'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('purple', 'Purple'),
        ('brown', 'Brown'),
        ('violet', 'Violet'),
        )

class ColorModel(models.Model):
    color= models.CharField(null=True, max_length=80,  choices=COLOR_CHOICES, blank=True, default=None)
    class Meta:
        db_table = 'ref_colors'
    
    def __str__(self):
        return "{}, {}".format(self.color)