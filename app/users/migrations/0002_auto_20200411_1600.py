# Generated by Django 3.0.1 on 2020-04-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='closed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=models.TextField(blank=True, max_length=180, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='doorService',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='emergency',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
