# Generated by Django 3.2.16 on 2022-12-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0005_auto_20221214_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]