# Generated by Django 2.2.3 on 2019-10-02 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190930_1017'),
        ('situacionesadms', '0020_auto_20190930_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='resolucion_viatico',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='No. Resolución (viáticos)'),
        ),
        migrations.CreateModel(
            name='Encargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funcionario_encargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Empleado')),
                ('solicitud', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='situacionesadms.Solicitud')),
            ],
        ),
    ]