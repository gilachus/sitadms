from django.db.models import Q
from django.shortcuts import render
from situacionesadms.models import Solicitud, SituacionAdministrativa


def estadisticas(request):
    solicitudes = Solicitud.objects.filter(estado=1)
    situaciones = SituacionAdministrativa.objects.all()
    total_tipo = {}
    for situacion in situaciones:
        total_tipo[situacion.nombre] = solicitudes.filter(situacion__slug=situacion.slug, estado=1).count()
    context = {
        'total_tipo': total_tipo,
        'total': solicitudes.count()
    }
    return render(request, 'estadisticas/estadisticas.html', context)


def ultimos_encargos(request):
    solicitudes_con_encargo = Solicitud.objects.filter(~Q(nombre_encargo=None), Q(estado=1))
    context={
        'encargos': solicitudes_con_encargo.order_by('-fecha_creacion')[0:30]
    }
    return render(request, 'estadisticas/ultimos_encargos.html', context)