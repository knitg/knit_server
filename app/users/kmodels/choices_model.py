from django.db import models

USER_ROLE_CHOICES = (
        (1, 'Customer'),
        (2, 'Super Admin'),
        (3, 'Admin'),
        (4, 'Manager'),
        (5, 'Developer'),
        (6, 'Owner'),
        (7, 'Sales Manger'),
        (8, 'Delivery'),
        )

GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Trans Gender'),
        )