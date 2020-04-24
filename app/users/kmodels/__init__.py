from .usertype_model import UserType

import os
import csv
from django.conf import settings
### REFERENCE USER TYPES ###
def create_user_types():
    print(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_user_type.csv'))
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_user_type.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                print(row)
                user_type, created = UserType.objects.get_or_create(
                    user_type=row[0],
                    description=row[1]
                )
                if created:
                    user_type.save() 
create_user_types()
