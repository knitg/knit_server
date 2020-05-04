# Generated by Django 3.0.1 on 2020-05-04 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaggamCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=80, null=True)),
                ('userId', models.IntegerField(default=None, null=True)),
                ('customizable', models.BooleanField(blank=True, default=False, null=True)),
                ('details', models.CharField(default=None, max_length=80, null=True)),
                ('category', models.ManyToManyField(default=None, null=True, to='products.Category')),
                ('images', models.ManyToManyField(blank=True, default=None, to='products.KImage')),
            ],
            options={
                'db_table': 'maggam_catalog',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FashionCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=80, null=True)),
                ('userId', models.IntegerField(default=None, null=True)),
                ('customizable', models.BooleanField(blank=True, default=False, null=True)),
                ('details', models.CharField(default=None, max_length=80, null=True)),
                ('category', models.ManyToManyField(default=None, null=True, to='products.Category')),
                ('images', models.ManyToManyField(blank=True, default=None, to='products.KImage')),
            ],
            options={
                'db_table': 'fashion_catalog',
                'managed': True,
            },
        ),
    ]
