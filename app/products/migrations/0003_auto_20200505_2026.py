# Generated by Django 3.0.1 on 2020-05-05 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_fashioncatalog_maggamcatalog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sub_Category',
            new_name='sub_category',
        ),
    ]
