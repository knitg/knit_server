from .color_model import ColorModel
from .sizes_model import SizeModel
from .material_model import MaterialModel

import os
import csv
from django.conf import settings

### REFERENCE COLORS ###
def create_colors():
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_colors.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                color, created = ColorModel.objects.get_or_create(
                    color=row[0]
                )
                if created:
                    print("REFERENCE COLORS CREATED")
                    color.save() 

create_colors()
### REFERENCE SIZES ###
def create_sizes():
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_sizes.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                size, created = SizeModel.objects.get_or_create(
                    size=row[0]
                )
                if created:
                    print("REFERENCE SIZES CREATED")
                    size.save() 

create_sizes()

### REFERENCE MATERIAL ###
def create_materials():
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_materials.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                material, created = MaterialModel.objects.get_or_create(
                    material=row[0]
                )
                if created:
                    print("REFERENCE MATERIALS CREATED")
                    material.save() 

create_materials()