from django.db.models import Q
from django.shortcuts import render
from situacionesadms.models import Solicitud, SituacionAdministrativa

class TipoSituacion(object):
    def __init__(self, nombre, cantidad, porcentaje):
        self.nombre = nombre
        self.cantidad = cantidad
        self.porcentaje = porcentaje

def estadisticas(request):
    solicitudes = Solicitud.objects.filter(estado=3)
    total=solicitudes.count()
    situaciones = SituacionAdministrativa.objects.all()
    total_tipo = []
    for situacion in situaciones:
        nombre = situacion.nombre
        cantidad = solicitudes.filter(situacion__slug=situacion.slug, estado=3).count()
        if total == 0:
            porcentaje=0
        else: 
            porcentaje = cantidad*100/total

        total_tipo.append(TipoSituacion(nombre, cantidad, porcentaje))
    context = {        
        'total': total,
        'total_tipo': total_tipo,
    }
    return render(request, 'estadisticas/estadisticas.html', context)


def ultimos_encargos(request):
    solicitudes_con_encargo = Solicitud.objects.filter(~Q(nombre_encargo=None), Q(estado=3))
    context={
        'encargos': solicitudes_con_encargo.order_by('-fecha_creacion')
    }
    return render(request, 'estadisticas/ultimos_encargos.html', context)