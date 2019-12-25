# KNIT API APPLICATION
Knit is complete stitching solution.

## PREREQUISITE
Python 3.x

## STEPS
Clone the repo and [cd] to the directory

Run below commands
```bash
1. pip install pipenv
2. pipenv shell
3. pip install -r requirements.txt
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py runserver
```

# HOW TO USE API 
### Below apis are handle CRUD operations

Api has 3 major categorys

1. /admin/ - It will handle the backend adminstration.
```python
With super user credentials we can enter into the admin site.
```
2. /user/  - It will handle user category apis(below end points available).

```python
GET /user/auth/users/ - Create user

GET /user/auth/jwt/create/ - Create access JWT token 

GET /user/auth/users/me/ - Get user information by passing the key (header: Authorization: JWT <access token>)

GET /user/auth/jwt/verify/ - Verify the access token valid (params: token: <access token>)

GET /user/auth/jwt/refresh/ - If access token invalid try to get another one with refresh (params: token: <access token>)

GET /user/user-list - Get user complete list

GET /user/address - address end point

GET /user/user-types - user types end point(eg: Guest, Customer, Tailor, Master, Boutique etc...)

GET /user/customer - Get customer or add customer or retrieve customer(/user/customer/<id>)

GET /user/vendor - Get Vendors or add vendors or retrieve vendors(/user/vendor/<id>)

```
3. /product/ - It will handle product apis.

```python
GET /product/stitch - Stitch category

GET /product/stitch-types - Stitch types (depends on [stitch])

GET /product/stitch-type/<stitch_id> - Get Stitch types against to stitch

GET /product/stitch-type-design - Stitch type design (depends on [stitch-types])

GET /product/product - Product api (vendor can add product)

GET /product/userproducts/<user_id> - Get products against to user

GET /product/stitchproducts/<stitch_id> - Get products against to Stitch category

GET /product/stitchtypeproducts/<stitch_type_id> - Get products against to Stitch type Category
 
```
