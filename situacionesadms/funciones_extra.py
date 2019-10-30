# from datetime import datetime as dt, timedelta
import os
from django.utils import timezone   
from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404
from users.models import Empleado
from django.db.models import Q
# -método nombre_aleatorio-
import string
import random
#
# -método update_name-
from uuid import uuid4
# 
# -método delete-
from django.core.files.storage import default_storage
from django.db.models import FileField
# 

ESTADO = [(0, "papelera"), (1, "en trámite"), (2, "corregir"), (3, "aprobada"), (4, "revocada"), (5, "rechazada")]


def delta_fechas(finicio, ffin):
    """intervalo de dias incluyendo el día inicial"""
    delta_fecha_dias = ffin - finicio
    return delta_fecha_dias.days+1

def nombre_aleatorio(n):
    letters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(letters) for i in range(n))
    return password

def update_filename(instance, filename, path="attached/"):
    # upload_to = path
    # ext = filename.split('.')[-1]
    # get filename
    # if instance.pk:
    #     filename = '{}.{}'.format(instance.pk, ext)
    # else:
        ## set filename as random string
    # filename = '{}.{}'.format(uuid4().hex, ext)
    upload_to = os.path.join(path,uuid4().hex)
    ## return the whole path to the file
    return os.path.join(upload_to, filename)

def borra_archivo(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)


def valida_empleado(peticion):
    """si es super usuario, si la cuenta esta activa, si esta asociado al modelo empleado"""
    if not peticion.user.is_active:
        messages.error(peticion, 'su cuenta ha sido desactivada')
        return False
    empleado = Empleado.objects.filter(user=peticion.user).first()
    if empleado:
        return True
    else:
        return False

def valida_acceso(peticion):
    if peticion.user.empleado.acceso != 1:
        return True
    else:
        return False
    

# ---------ejemplo timezone
# date_filed = models.DateField(default=timezone.now)
# ---------ejemplo naive to aware
# import pytz
# naive = datetime.now()
# aware = naive.replace(tzinfo=pytz.UTC)


# def file_cleanup(sender, **kwargs):
#     for fieldname in sender._meta.get_all_field_names():
#         try:
#             field = sender._meta.get_field(fieldname)
#         except:
#             field = None
#             if field and isinstance(field, FileField):
#                 inst = kwargs['instance']
#                 f = getattr(inst, fieldname)
#                 m = inst.__class__._default_manager
#                 if hasattr(f, 'path') and os.path.exists(f.path) and not m.filter(**{'%s__exact' % fieldname: getattr(inst, fieldname)}).exclude(pk=inst._get_pk_val()):
#                     try:
#                         default_storage.delete(f.path)
#                     except:
#                         pass

def notas_situacion(slug):
    nota = {"permiso-remunerado": '''"En virtud de esta situación administrativa, el empleado puede solicitar por
            escrito permiso remunerado hasta por tres (3) días hábiles cuando medie
            justa causa. Corresponde al nominador o a su delegado la facultad de
            autorizar o negar los permisos". -ABC de situaciones administrativas''',

            "permiso-sindical": '''"El nominador o el funcionario que este delegue para el efecto, reconocerá
            mediante acto administrativo los permisos sindicales, de las organizaciones
            sindicales de primero, segundo o tercer grado, previa solicitud de las
            organizaciones sindicales precisando:
            1. Permisos necesarios para el cumplimiento de su gestión
            2. Nombre de los representantes
            3. Finalidad
            4. Duración periódica y
            5. Distribución". -ABC de situaciones administrativas''',
                # "permiso-laboral": PermisoLaboralForm,
                # "comision-de-servicio": ComisionForm,
                # "comision-de-estudio-menor-6-meses": ComisionForm,
                # "comision-de-estudio-mayor-6-meses": ComisionForm,
                # "comision-menor-a-15-dias-viaticos": ComisionViaticosForm,
                # "permiso-academico-compensado-interno": JustificacionYEncargoForm,
                # "permiso-academico-compensado-externo": JustificacionYEncargoForm,
                # "permiso-para-ejercer-docencia-universitaria": PermisoEjercerDocenciaForm,
                # "licencia-especial-para-docentes": BasicForm,
                # "licencia-ordinaria-no-remunerada": BasicForm,
                # "licencia-no-remunerada-para-adelantar-estudios": BasicForm,
                # "reserva-de-vacaciones": ReservaVacacionesForm,
                # "disfrute-de-vacaciones-reservadas": DisfruteVacacionesForm,
                # "reserva-de-dias-compensatorios": BasicForm,
                # "disfrute-de-dias-compensatorios": BasicForm,
                # "licencia-por-enfermedad": JustificacionYEncargoForm,
                # "licencia-por-maternidad": JustificacionYEncargoForm,
                # "licencia por paternidad": JustificacionYEncargoForm,
                # "licencia por luto": JustificacionYEncargoForm
                }
    if slug in nota:
        return nota[slug]
    else:
        return "no hay recomendaciones"
