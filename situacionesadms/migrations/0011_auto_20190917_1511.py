# Generated by Django 2.2.3 on 2019-09-17 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0010_auto_20190910_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='reintegro',
            name='cumplido',
            field=models.FileField(default=None, upload_to='cumplidos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reintegro',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reintegro',
            name='fecha_modificaion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='reintegro',
            name='situacion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='situacionesadms.Solicitud'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitud',
            name='modifica_a1',
            field=models.CharField(default=None, max_length=20, verbose_name='Modifica a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitud',
            name='modifica_a2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='situacionesadms.Solicitud'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='dias_permiso',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='No. días'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='no_reservas_personal',
            field=models.ManyToManyField(blank=True, related_name='solicitud_reserva', to='situacionesadms.Solicitud'),
        ),
    ]