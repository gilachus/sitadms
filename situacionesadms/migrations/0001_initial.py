# Generated by Django 2.2.3 on 2019-08-23 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reintegro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SituacionAdministrativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('dias_anticipacion', models.IntegerField(default=0)),
                ('max_horas_mensuales', models.IntegerField(default=0)),
                ('max_dias_otorgables', models.IntegerField(default=0)),
                ('max_meses_otorgables', models.IntegerField(default=0)),
                ('dias_reintegro', models.IntegerField(default=0)),
                ('dias_prorroga', models.IntegerField(default=0)),
                ('meses_prorroga', models.IntegerField(default=0)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificaion', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('ultimo_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Situaciones Administrativas',
            },
        ),
        migrations.CreateModel(
            name='TipoResolucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Resoluciones',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.PositiveIntegerField(choices=[(0, 'papelera'), (1, 'tramite'), (2, 'corregir'), (3, 'aprobada'), (4, 'revocada'), (5, 'rechazada')], default=1)),
                ('fecha_i', models.DateField(verbose_name='Fecha inicio')),
                ('fecha_f', models.DateField(verbose_name='Fecha fin')),
                ('dias_permiso', models.PositiveIntegerField(blank=True, null=True, verbose_name='Días permiso')),
                ('justificacion', models.TextField(blank=True, help_text='describa los motivos de su solicitud', null=True)),
                ('ciudad', models.CharField(max_length=50)),
                ('pais', models.CharField(max_length=50, verbose_name='País')),
                ('asiste_en_calidad', models.PositiveIntegerField(choices=[(1, 'Estudiante'), (2, 'Asistente'), (2, 'Ponente'), (3, 'Conferencista'), (4, 'Otro')], default=1)),
                ('soportes', models.FileField(blank=True, null=True, upload_to='attached')),
                ('convenio', models.FileField(blank=True, null=True, upload_to='agreement')),
                ('requiere_encargo', models.BooleanField(default=False)),
                ('nombre_encargo', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido_encargo', models.CharField(blank=True, max_length=50, null=True)),
                ('cargo_encargo', models.CharField(blank=True, max_length=100, null=True)),
                ('no_reserva_rectoria', models.CharField(blank=True, max_length=20, null=True, verbose_name='No. reserva rectoría')),
                ('no_reserva_personal', models.CharField(blank=True, max_length=50, null=True)),
                ('resolucion_vaciones', models.CharField(blank=True, max_length=20, null=True)),
                ('no_dias_a_reservar', models.PositiveIntegerField(blank=True, null=True)),
                ('no_dias_a_disfrutar', models.PositiveIntegerField(blank=True, null=True)),
                ('dias_pendientes2', models.PositiveIntegerField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificaion', models.DateTimeField(auto_now=True)),
                ('revisar_encargo', models.BooleanField(default=False)),
                ('revisar_planeacion', models.BooleanField(default=False)),
                ('check_jefe_inmediato', models.BooleanField(default=False)),
                ('check_asistente_RH', models.BooleanField(default=False)),
                ('check_asistente2_RH', models.BooleanField(default=False)),
                ('check_asistente_AL', models.BooleanField(default=False)),
                ('checK_jefe_AL', models.BooleanField(default=False)),
                ('check_licencias', models.BooleanField(default=False)),
                ('check_jefe_RH', models.BooleanField(default=False)),
                ('check_planeacion', models.BooleanField(default=False)),
                ('check_seleccion', models.BooleanField(default=False)),
                ('check_vice_doc', models.BooleanField(default=False)),
                ('check_vice_adm', models.BooleanField(default=False)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('empleado', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.Empleado')),
                ('no_reservas_personal', models.ManyToManyField(to='situacionesadms.Solicitud')),
                ('situacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='situacionesadms.SituacionAdministrativa')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes',
            },
        ),
        migrations.CreateModel(
            name='Resolucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=50, unique=True)),
                ('fecha', models.DateField()),
                ('documento', models.FileField(blank=True, null=True, upload_to='resolutions')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='situacionesadms.TipoResolucion')),
            ],
            options={
                'verbose_name_plural': 'Resoluciones',
            },
        ),
        migrations.CreateModel(
            name='DetalleRechazo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fecha_update', models.DateTimeField(auto_now=True)),
                ('solicitud', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='situacionesadms.Solicitud')),
            ],
        ),
    ]
