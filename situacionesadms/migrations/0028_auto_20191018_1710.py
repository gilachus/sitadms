# Generated by Django 2.2.3 on 2019-10-18 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('situacionesadms', '0027_auto_20191016_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallerechazo',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='detallerechazo',
            name='motivo',
            field=models.TextField(help_text='<em>Describa las razones por las cual se rechaza</em>'),
        ),
    ]