# Generated by Django 2.2.3 on 2019-10-25 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0038_auto_20191025_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitud',
            old_name='check_licencias',
            new_name='check_abogado_AL',
        ),
    ]