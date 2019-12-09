# Generated by Django 2.2.7 on 2019-12-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0043_solicitud_revisar_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='reintegro',
            name='pendiente_soporte',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reintegro',
            name='seguimiento',
            field=models.PositiveIntegerField(choices=[(0, 'papelera'), (1, 'tramite'), (2, 'corregida_modificada'), (3, 'aprobada'), (4, 'revocada'), (5, 'rechazada')], default=1),
        ),
    ]
