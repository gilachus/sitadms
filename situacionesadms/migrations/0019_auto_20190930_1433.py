# Generated by Django 2.2.3 on 2019-09-30 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situacionesadms', '0018_auto_20190930_1308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitud',
            old_name='checK_jefe_AL',
            new_name='check_jefe_AL',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='cargo_encargo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cargo Funcionario'),
        ),
    ]
