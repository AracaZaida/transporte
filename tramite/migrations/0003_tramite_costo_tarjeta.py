# Generated by Django 5.1.7 on 2025-05-27 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramite', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='costo_tarjeta',
            field=models.IntegerField(default=40),
        ),
    ]
