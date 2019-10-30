from django.db.models import Q
from .models import Solicitud


def conteo_solicitudes_entrantes(acceso):
    base = Solicitud.objects.all().filter(estado=1)
    solicitudes = Solicitudes.objects.none()
    ## Vacaciones
    if user.empleado.tipo_acceso == 6: 
        solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
        Q(situacion__nombre="disfrute de vacaciones reservadas"), Q(check_asistente_al=True))
    ## Jefe Vacaciones
    elif user.empleado.tipo_acceso == 7:
        solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
        Q(situacion__nombre="reserva de vacaciones"), Q(check_asistente_AL=True) & Q(check_jefe_AL=False))
    ## luto enfermedad paternidad maternidad 
    elif user.empleado.tipo_acceso==5:
        solicitudes = base.filter(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
        Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto")).exclude(Q(check_licencias=True))
    ## Asistente OAGHDP
    elif user.empleado.tipo_acceso == 2:
        solicitudes = base.exclude(Q(situacion__nombre="reserva de vacaciones") | Q(situacion__nombre="disfrute de vacaciones reservadas") , 
        Q(check_jefe_AL=False) & Q(check_jefe_AL=False)).exclude(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
        Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto"), Q(check_licencias=False))
    ## Jefe OAGHDP
    elif user.empleado.tipo_acceso == 4:
        solicitudes = base.filter(Q(check_asistente_OAGHDP), Q(requiere_estudio_perfil=True) & Q(check_seleccion=True))
    ## vice doc
    elif user.empleado.tipo_acceso == 10:
        solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & q(va_a_vice=1))
    ## vice adm
    elif user.empleado.tipo_acceso == 11:
        solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & q(va_a_vice=2))
    
    return solicitudes.count()