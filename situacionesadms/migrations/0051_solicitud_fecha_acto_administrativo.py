# Generated by Django 2.2.7 on 2019-12-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0050_auto_20191213_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='fecha_acto_administrativo',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
