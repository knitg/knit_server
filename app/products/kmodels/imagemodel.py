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

def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')

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
            try:
                pil_img = Image.open(self.image)
            except Exception:
                pil_img = Image.open(self.image.name)
            
            # resize image to proportionate
            im = resize(pil_img, 800, 800)
            output = BytesIO()
            # #after modifications, save it to the output
            im.save(output, format='JPEG', quality=80)
            
            #change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output,'ImageField', "%s.png" %self.image.name.split('.')[0], 'image/png', sys.getsizeof(output), None)

        super(KImage, self).save()

    def __str__(self):
        return self.image

