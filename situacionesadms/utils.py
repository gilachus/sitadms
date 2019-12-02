from django.db.models import Q
from .models import Solicitud
from .forms import (BasicForm, ConJustificacionForm, ConEncargoForm, JustificacionYEncargoForm, 
                    PermisoRemuneradoForm, PermisoLaboralForm, ComisionForm, ComisionViaticosForm, 
                    ReservaVacacionesForm, DisfruteVacacionesForm, 
                    ReservaCompensatorio, DisfruteCompensatorio,
                    RechazoForm, ComisionMayorSeisSabaticoForm) 
from .form_blank import *

def retorna_form(slug):
    """retorna un form dependiendo de la situacion adm que quiere diligenciar el usuario"""

    dict_forms = {"permiso-remunerado": PermisoRemuneradoForm,
                "permiso-sindical": JustificacionYEncargoForm,
                "permiso-laboral": PermisoLaboralForm,
                "comision-de-servicio": ComisionForm,
                "comision-de-estudio-menor-6-meses": ComisionForm,
                "comision-de-estudio-mayor-6-meses": ComisionMayorSeisSabaticoForm, #interno
                "ano-sabatico": ComisionMayorSeisSabaticoForm, #interno      
                "comision-menor-a-15-dias-viaticos": ComisionViaticosForm,
                "permiso-academico-compensado-interno": JustificacionYEncargoForm,
                "permiso-academico-compensado-externo": JustificacionYEncargoForm,
                "permiso-para-ejercer-docencia-universitaria": JustificacionYEncargoForm,
                "licencia-especial-para-docentes": BasicForm,
                "licencia-ordinaria-no-remunerada": BasicForm,
                "licencia-no-remunerada-para-adelantar-estudios": BasicForm,
                "reserva-de-vacaciones": ReservaVacacionesForm,
                "disfrute-de-vacaciones-reservadas": DisfruteVacacionesForm,
                "reserva-de-dias-compensatorios": ReservaCompensatorio,
                "disfrute-de-dias-compensatorios": DisfruteCompensatorio,
                "licencia-por-enfermedad": ConEncargoForm,
                "licencia-por-maternidad": ConEncargoForm,
                "licencia-por-paternidad": ConEncargoForm,
                "licencia-por-luto": ConEncargoForm,
                "licencia-deportiva":JustificacionYEncargoForm,
                }
    if slug in dict_forms:
        return dict_forms[slug]
    else:
        return BasicForm

# def conteo_solicitudes_entrantes(acceso):
#     base = Solicitud.objects.all().filter(estado=1)
#     solicitudes = Solicitudes.objects.none()
#     ## Vacaciones
#     if user.empleado.tipo_acceso == 6: 
#         solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
#         Q(situacion__nombre="disfrute de vacaciones reservadas"), Q(check_asistente_al=True))
#     ## Jefe Vacaciones
#     elif user.empleado.tipo_acceso == 7:
#         solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
#         Q(situacion__nombre="reserva de vacaciones"), Q(check_asistente_AL=True) & Q(check_jefe_AL=False))
#     ## luto enfermedad paternidad maternidad 
#     elif user.empleado.tipo_acceso==5:
#         solicitudes = base.filter(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
#         Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto")).exclude(Q(check_licencias=True))
#     ## Asistente OAGHDP
#     elif user.empleado.tipo_acceso == 2:
#         solicitudes = base.exclude(Q(situacion__nombre="reserva de vacaciones") | Q(situacion__nombre="disfrute de vacaciones reservadas") , 
#         Q(check_jefe_AL=False) & Q(check_jefe_AL=False)).exclude(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
#         Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto"), Q(check_licencias=False))
#     ## Jefe OAGHDP
#     elif user.empleado.tipo_acceso == 4:
#         solicitudes = base.filter(Q(check_asistente_OAGHDP), Q(requiere_estudio_perfil=True) & Q(check_seleccion=True))
#     ## vice doc
#     elif user.empleado.tipo_acceso == 10:
#         solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & q(va_a_vice=1))
#     ## vice adm
#     elif user.empleado.tipo_acceso == 11:
#         solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & q(va_a_vice=2))
    
#     return solicitudes.count()


def retorna_form_blank(slug):
    """retorna un form con soportes y convenio opcionales"""

    dict_forms = {"permiso-remunerado": PermisoRemuneradoFormBlank,
                "permiso-sindical": JustificacionYEncargoFormBlank,
                "permiso-laboral": PermisoLaboralFormBlank,
                "comision-de-servicio": ComisionFormBlank,
                "comision-de-estudio-menor-6-meses": ComisionFormBlank,
                "comision-de-estudio-mayor-6-meses": ComisionMayorSeisSabaticoFormBlank, #interno
                "ano-sabatico": ComisionMayorSeisSabaticoFormBlank, #interno      
                "comision-menor-a-15-dias-viaticos": ComisionViaticosFormBlank,
                "permiso-academico-compensado-interno": JustificacionYEncargoFormBlank,
                "permiso-academico-compensado-externo": JustificacionYEncargoFormBlank,
                "permiso-para-ejercer-docencia-universitaria": JustificacionYEncargoFormBlank,
                "licencia-especial-para-docentes": BasicFormBlank,
                "licencia-ordinaria-no-remunerada": BasicFormBlank,
                "licencia-no-remunerada-para-adelantar-estudios": BasicFormBlank,
                "reserva-de-vacaciones": ReservaVacacionesFormBlank,
                "disfrute-de-vacaciones-reservadas": DisfruteVacacionesFormBlank,
                "reserva-de-dias-compensatorios": ReservaCompensatorioBlank,
                "disfrute-de-dias-compensatorios": DisfruteCompensatorioBlank,
                "licencia-por-enfermedad": ConEncargoFormBlank,
                "licencia-por-maternidad": ConEncargoFormBlank,
                "licencia-por-paternidad": ConEncargoFormBlank,
                "licencia-por-luto": ConEncargoFormBlank,
                "licencia-deportiva":JustificacionYEncargoFormBlank,
                }
    if slug in dict_forms:
        return dict_forms[slug]
    else:
        return BasicForm