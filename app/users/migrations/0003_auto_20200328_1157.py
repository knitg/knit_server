# Generated by Django 3.0.1 on 2020-03-28 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200328_0119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='images',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_role',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
    ]