from django.db.models import Q
from django.shortcuts import render
from situacionesadms.models import Solicitud
# Create your views here.
def estadisticas(request):
    pass

def ultimos_encargos(request):
    solicitudes_con_encargo = Solicitud.objects.filter(~Q(nombre_encargo=None), Q(estado=3))
    context={
        'encargos': solicitudes_con_encargo.order_by('-fecha_creacion')[0:30]
    }
    return render(request, 'estadisticas/ultimos_encargos.html', context)