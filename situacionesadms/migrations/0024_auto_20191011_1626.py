# Generated by Django 2.2.3 on 2019-10-11 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0023_auto_20191011_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='asiste_en_calidad',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Estudiante'), (2, 'Asistente'), (2, 'Ponente'), (3, 'Conferencista'), (4, 'Otro')], null=True),
        ),
    ]
