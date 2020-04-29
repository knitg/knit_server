from ..kmodels.usertype_model import UserType

from django.db import connection
import os
import csv
from django.conf import settings
from ..kserializers.user_serializer import UserSerializer
from ..kserializers.address_serializer import AddressSerializer
from ..kserializers.vendor_serializer import VendorSerializer

def checkTables(tablename):
    cursor = connection.cursor()
    stmt = "SHOW TABLES LIKE '%s' "% ('%'+str(tablename)+'%')
    cursor.execute(stmt)
    return cursor.fetchone()

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
   

### Users load from CSV ###
def create_users():
    print(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_users.csv'))
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_users.csv')) as f:
        reader = csv.reader(f)
        users = []
        profile = []
        for i, row in enumerate(reader):
            print(row)
            if (i >= 1 and row):
                admin = False
                if row[4]:
                    admin = True if (row[4] and row[4] == '1') else False 
                #======================== CREATE USER ========================#
                user_data = {}
                user_data['phone'] = row[1]
                user_data['email'] = row[2]
                user_data['password'] = row[3]
                user_data['username'] = row[0]
                user_data['is_admin'] = admin

                user_serializer = UserSerializer(data= {'user': user_data, 'profile': {}, 'data':user_data})
                if user_serializer.is_valid():
                    user_serializer.save()
                else:
                    print("USER ERROR ", user_serializer.errors)


### ADDRESS load from CSV ###
def create_address():
    print(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_address.csv'))
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_address.csv')) as f:
        reader = csv.reader(f)
        users = []
        profile = []
        for i, row in enumerate(reader):
            print(row)
            if (i >= 1 and row):
                #======================== CREATE ADDRESS ========================#
                try:
                    address_data = {}
                    address_data['address_type'] = row[0] # "address_type"
                    address_data['house_name'] = row[1] #"house_name"
                    address_data['address_line1'] = row[2] #"address_line1"
                    address_data['address_line2'] = row[3] #"address_line2"
                    address_data['area_name'] = row[4] # "area_name"
                    address_data['landmark'] = row[5] # "landmark"
                    address_data['postalCode'] = row[6] # "postalCode"
                    address_data['latitude'] = row[7] # "latitude"
                    address_data['longitude'] = row[8] # "longitude"
                    address_data['geoAddress'] = row[9] # "geoAddress"
                    address_data['city'] = row[10] # "city"
                    address_data['state'] = row[11] # "state"
                    address_data['country'] = row[12] # "country"
                    address_serializer = AddressSerializer(data= address_data)
                except ValueError as e:
                    print("VALUE ERROR ", e)
                    return  ValueError("Something went wrong with values", e)
                except IndexError as e:
                    print("Index ERROR ", e)
                    return KeyError("Something went wrong with keys", e)
                except AttributeError as e:
                    print("Attribute error", e)
                    return AttributeError("attribute error")
                except TypeError as e:
                    print("TYPE ERROR", e)
                    return TypeError("TYPE ERROR {}".format(e))
                try:
                    address_serializer.is_valid()
                    address_serializer.save()
                except Exception:
                    print("\n ADDRESS ERROR ", address_serializer.errors)



### REFERENCE VENDOR USERS ###
def create_vendor_users():
    print("\n\n\n\n")
    print(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_vendor_users.csv'))
    with open(os.path.join(settings.BASE_DIR, 'db_scripts', 'ref_vendor_users.csv')) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if (i >= 1 and row):
                print(row)
                user_data = {}
                user_data['username'] = row[0]
                user_data['phone'] = row[1]
                user_data['email'] = row[2]
                user_data['password'] = row[3]
                vendor_details = {}
                vendor_details['name'] = row[4]
                vendor_details['masters'] = int(row[7])
                vendor_details['doorService'] = row[6]
                vendor_details['emergency'] = row[5]

                vendor_serializer = VendorSerializer(data= {'user': user_data, 'vendor': vendor_details, 'data': vendor_details})
                if vendor_serializer.is_valid():
                    vendor_serializer.save()
                else:
                    print("VENDOR Error", vendor_serializer.errors)


#### IF TABLE WERE PRESENT IN DB #####
if checkTables('ref_user_types') is not None: 
    create_user_types()
if checkTables('knit_user'):
    create_users() 
if checkTables('ref_address'):
    create_address()
