# Generated by Django 4.1.3 on 2022-12-11 02:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('personal_id_number', models.CharField(max_length=50)),
                ('id_number', models.CharField(max_length=50)),
                ('marital_status', models.IntegerField(choices=[(0, 'Belum Menikah'), (1, 'Menikah'), (2, 'Cerai')], default=0)),
                ('religion', models.IntegerField(choices=[(0, 'Islam'), (1, 'Kristen'), (2, 'Katolik'), (3, 'Hindu'), (4, 'Budha'), (5, 'Konghucu')], default=0)),
                ('job_status', models.IntegerField(choices=[(0, 'Tetap'), (1, 'Kontrak')], default=0)),
                ('joint_date', models.DateField()),
                ('birth_date', models.DateField()),
                ('birth_place', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('address_by_id', models.CharField(max_length=255)),
                ('address_by_domicile', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.position')),
            ],
        ),
    ]
