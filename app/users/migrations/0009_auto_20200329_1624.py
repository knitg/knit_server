# Generated by Django 3.0.1 on 2020-03-29 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200329_1104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True, 'ordering': ['-created_at', '-updated_at'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
