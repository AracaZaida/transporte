# Generated by Django 5.1.7 on 2025-05-22 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('flag', models.CharField(choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')], default='nuevo', max_length=20)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehiculo.marca'),
        ),
    ]
