# Generated by Django 2.2.3 on 2019-08-23 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0002_auto_20190823_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='nombre_del_evento',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]