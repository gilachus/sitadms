# Generated by Django 2.2.3 on 2019-08-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0004_auto_20190826_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='convenio',
            field=models.FileField(blank=True, null=True, upload_to='agreement/%Y'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='soportes',
            field=models.FileField(blank=True, null=True, upload_to='attached/%Y'),
        ),
    ]
