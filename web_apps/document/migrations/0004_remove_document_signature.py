# Generated by Django 4.1.3 on 2022-12-11 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_document_signature_alter_document_document_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='signature',
        ),
    ]
