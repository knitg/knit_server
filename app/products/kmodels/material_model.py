from django.db import models

class MaterialModel(models.Model):
    material= models.CharField(null=True, max_length=100,  blank=True, default=None)
    code= models.CharField(null=True, max_length=30,  blank=True, default=None)
    class Meta:
        db_table = 'ref_materials'
    
    def __str__(self):
        return self.code