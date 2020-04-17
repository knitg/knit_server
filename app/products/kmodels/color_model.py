from django.db import models

class ColorModel(models.Model):
    color= models.CharField(null=True, max_length=30,  blank=True, default=None)
    code= models.CharField(null=True, max_length=30,  blank=True, default=None)
    class Meta:
        db_table = 'ref_colors'
    
    def __str__(self):
        return self.code