from django.db import models
import re

class SizeModel(models.Model):
    size= models.CharField(null=True, max_length=30,  blank=True, default=None)
    code= models.CharField(null=True, max_length=30,  blank=True, default=None)
    class Meta:
        db_table = 'ref_sizes'
    
    def save(self, *args, **kwargs):
        if not self.size:
            raise ValueError("Please enter Size")
        else:
            replaced_txt = re.sub(r'\W+', '-', self.size)
            self.code = replaced_txt.upper()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.code
