# Generated by Django 4.2.6 on 2023-10-28 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peticiones', '0002_rename_pqr_peticion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peticion',
            name='tipo_solicitud',
            field=models.CharField(choices=[('Petición', 'Petición'), ('Queja', 'Queja'), ('Reclamo', 'Reclamo')], max_length=8),
        ),
    ]
