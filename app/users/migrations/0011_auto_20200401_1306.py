# Generated by Django 3.0.1 on 2020-04-01 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_kaddress_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
