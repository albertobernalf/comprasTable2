# Generated by Django 3.2 on 2023-04-11 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0012_articulos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='articulo',
            field=models.CharField(max_length=300),
        ),
    ]
