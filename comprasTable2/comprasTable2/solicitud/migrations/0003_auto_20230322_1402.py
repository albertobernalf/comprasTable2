# Generated by Django 3.2 on 2023-03-22 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0002_auto_20230321_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudesdetalle',
            name='estadosAlmacen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eestadosAlmacen', to='solicitud.estadosalmacen'),
        ),
        migrations.AlterField(
            model_name='solicitudesdetalle',
            name='usuarioResponsableAlmacen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uusuariosResponsableAlmacen', to='solicitud.usuarios'),
        ),
        migrations.AlterField(
            model_name='solicitudesdetalle',
            name='usuarioResponsableCompra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uusuariosResponsableCompra', to='solicitud.usuarios'),
        ),
        migrations.AlterField(
            model_name='solicitudesdetalle',
            name='usuarioResponsableValidacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='uusuariosResponsable', to='solicitud.usuarios'),
        ),
    ]
