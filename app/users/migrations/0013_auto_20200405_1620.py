# Generated by Django 3.0.1 on 2020-04-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200405_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
    ]
