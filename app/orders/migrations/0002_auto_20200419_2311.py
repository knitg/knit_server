# Generated by Django 3.0.1 on 2020-04-19 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stitchorder',
            name='expected_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
