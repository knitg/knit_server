# Generated by Django 3.0.1 on 2020-05-09 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='address',
            field=models.ManyToManyField(blank=True, default=None, to='users.Address'),
        ),
    ]
