# Generated by Django 2.2.3 on 2019-09-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190920_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='tipo_acceso',
            field=models.IntegerField(choices=[(1, 'simple'), (2, 'asistente_OAGHDP'), (3, 'convenios_OAGHDP'), (4, 'jefe_OAGHDP'), (5, 'luto_enfermedad_paternidad_maternidad_AL'), (6, 'vaciones_AL'), (7, 'jefe_AL'), (8, 'seleccion'), (9, 'planeacion'), (10, 'vice_adm'), (11, 'vice_doc'), (12, 'comunicacion_AL')], default=1),
        ),
    ]