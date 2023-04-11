# Generated by Django 3.2 on 2023-04-11 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0011_alter_solicitudesdetalle_especificacionestecnicas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codregArticulo', models.CharField(max_length=30, unique=True)),
                ('articulo', models.CharField(max_length=300, unique=True)),
                ('estadoreg', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
            ],
        ),
    ]
