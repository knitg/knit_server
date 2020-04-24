from django.db import models
import re

class ColorModel(models.Model):
    color= models.CharField(null=True, max_length=30,  blank=True, default=None)
    code= models.CharField(null=True, max_length=30,  blank=True, default=None)
    class Meta:
        db_table = 'ref_colors'
    
    def save(self, *args, **kwargs):
        if not self.color:
            raise ValueError("Please enter color")
        else:
            replaced_txt = re.sub(r'\W+', '-', self.color)
            self.code = replaced_txt.upper()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.code