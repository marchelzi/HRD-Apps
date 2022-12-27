# Generated by Django 4.1.3 on 2022-12-11 02:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadQuarter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('initial', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=15)),
                ('br_type', models.IntegerField(choices=[(0, 'Dalam Kota'), (1, 'Luar Kota')], default=0)),
                ('address', models.CharField(max_length=255)),
                ('headquarter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch.headquarter')),
                ('person_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pic', to='employee.employee')),
            ],
        ),
    ]