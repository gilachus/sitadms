# Generated by Django 2.2.3 on 2019-09-17 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190823_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='tipo_acceso',
            field=models.IntegerField(choices=[(0, 'restringido'), (1, 'simple'), (2, 'asistenteOAGHDP'), (3, 'jefeOAGHDP'), (4, 'licencias'), (5, 'asistenteAL'), (6, 'jefeAL'), (7, 'seleccion'), (8, 'vice_adm'), (9, 'vice_doc')], default=1),
        ),
    ]
