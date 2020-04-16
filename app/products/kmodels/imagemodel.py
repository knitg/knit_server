from django.db import models

from datetime import datetime
from django.utils.timezone import now

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
def uploadFolder(instance, filename):
    imgpath= '/'.join(['images', str(instance.source), filename])
    return imgpath

class KImage(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=uploadFolder, max_length=254, blank=True, null=True)
    source = models.CharField(blank=True, null=True, default='', max_length=50)
    size = models.IntegerField(blank=True, null=True, default=0)
    class Meta:
        db_table = 'knit_product_image'
        managed = True

    def save(self, **kwargs):
        if self.image:
            #Opening the uploaded image
            im = Image.open(self.image)
            output = BytesIO()
            # #Resize/modify the image
            # im = im.resize((800, 600), Image.ANTIALIAS)
            # #after modifications, save it to the output
            im.save(output, format='PNG', quality=100)
            
            #change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output,'ImageField', "%s.png" %self.image.name.split('.')[0], 'image/png', sys.getsizeof(output), None)

        super(KImage, self).save()

    def __str__(self):
        return self.image

