# Generated by Django 4.2.6 on 2023-10-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0006_alter_crear_estrategia_timeframe'),
    ]

    operations = [
        migrations.AddField(
            model_name='estrategia',
            name='codigo_python',
            field=models.TextField(blank=True, null=True),
        ),
    ]
