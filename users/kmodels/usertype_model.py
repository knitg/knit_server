from django.db import models

class KUserType(models.Model):    
    user_type= models.CharField(null=True, max_length=80,  default=None)  
    description = models.CharField(max_length=150, blank=True, null=True)
    class Meta:
        db_table = 'knit_user_type'
        managed = True
        verbose_name = 'Knit User type'
        verbose_name_plural = 'Knit User types'
    
    def __str__(self):
        return self.type
