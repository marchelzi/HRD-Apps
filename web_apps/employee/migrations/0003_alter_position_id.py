# Generated by Django 4.1.3 on 2022-12-11 03:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]