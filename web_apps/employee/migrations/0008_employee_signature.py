# Generated by Django 4.1.3 on 2022-12-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_alter_employee_id_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to='signatures'),
        ),
    ]