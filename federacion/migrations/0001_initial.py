# Generated by Django 5.1.7 on 2025-05-22 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Federacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('celular', models.CharField(blank=True, max_length=15, null=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('flag', models.CharField(choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')], default='nuevo', max_length=20)),
            ],
        ),
    ]
