# Generated by Django 3.0.1 on 2020-04-27 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200427_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stitch_type_design',
        ),
        migrations.DeleteModel(
            name='StitchTypeDesign',
        ),
    ]
