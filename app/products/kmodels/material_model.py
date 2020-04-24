from django.db import models
import re

class MaterialModel(models.Model):
    material= models.CharField(null=True, max_length=100,  blank=True, default=None)
    code= models.CharField(null=True, max_length=30,  blank=True, default=None)
    class Meta:
        db_table = 'ref_materials'
     
    def save(self, *args, **kwargs):
        if not self.material:
            raise ValueError("Material is not updated")
        else:
            replaced_txt = re.sub(r'\W+', '-', self.material)
            self.code = replaced_txt.upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.code