# Generated by Django 3.0.1 on 2020-03-25 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200325_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
