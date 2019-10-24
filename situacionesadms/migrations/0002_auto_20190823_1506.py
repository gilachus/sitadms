# Generated by Django 2.2.3 on 2019-08-23 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resolucion',
            name='fecha_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='resolucion',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='situacionesadms.TipoResolucion'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='justificacion',
            field=models.TextField(blank=True, help_text='Describa su solicitud', null=True),
        ),
    ]
