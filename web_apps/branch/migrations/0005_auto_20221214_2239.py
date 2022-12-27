# Generated by Django 3.2.16 on 2022-12-14 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_employee_signature'),
        ('branch', '0004_headquarter_created_at_headquarter_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='br_type',
            field=models.IntegerField(choices=[(0, 'Dalam Kota'), (1, 'Luar Kota')], default=0, verbose_name='Branch Type'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='initial',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='person_in_charge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pic', to='employee.employee'),
        ),
        migrations.AlterField(
            model_name='headquarter',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='branch',
            unique_together={('name', 'initial')},
        ),
    ]