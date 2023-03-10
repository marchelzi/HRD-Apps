# Generated by Django 4.1.3 on 2022-12-11 02:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0002_alter_branch_person_in_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branch',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
