from django.db import models
from .timestamp_model import TimestampedModel

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def nameFile(instance, filename):
    imgpath= '/'.join(['user_images', str(instance.source), filename])
    return imgpath

class KImage(TimestampedModel):
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=nameFile, max_length=254, blank=False, null=False, default=None)
    source = models.CharField(blank=True, null=True, default='customer', max_length=50)
    size = models.IntegerField(blank=True, null=True, default=0)
    class Meta:
        db_table = 'knit_image'
        managed = True

    def save(self, **kwargs):
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
