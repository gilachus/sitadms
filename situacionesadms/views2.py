from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Solicitud, Reintegro
from .forms import ReintegroForm
from .funciones_extra import SEGUIMIENTO, valida_empleado, valida_acceso


# views para los reintegros
@login_required
def llenar_reintegro(request, id_solicitud):
    if not valida_empleado(request):
        return redirect('users:inicio')
    situacion_objetivo = get_object_or_404(Solicitud, pk=id_solicitud)
    form = ReintegroForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.situacion = situacion_objetivo
            filepath = request.FILES.get('cumplido', False)
            if not filepath:
                instancia.pendiente_cumplido = True
            instancia.save()
            messages.success(request, "Solicictud de reintegro enviada.")
            return redirect('situacionesadms:mis_solicitudes')

    context = {
        'form': form,
        'situacion_objetivo': situacion_objetivo
    }
    return render(request, 'situacionesadms/llenar_reintegro.html', context)

@login_required
def reintegros_entrantes(request):
    """revisar reintegros en trámite"""
    if not valida_acceso(request):
        return redirect
    rlistado = None
    if request.user.empleado.tipo_acceso==2:
        rlistado = Reintegro.objects.filter(seguimiento=1).filter(check_asistente_OAGHDP=False).order_by('-fecha_creacion')
    if request.user.empleado.tipo_acceso==4:
         rlistado = Reintegro.objects.filter(seguimiento=1).filter(check_asistente_OAGHDP=True, check_jefe_OAGHDP=False).order_by('-fecha_creacion')
    print(rlistado)
    seguimiento = SEGUIMIENTO
    context={
        'rlistado': rlistado,
        'seguimiento': seguimiento
    }
    return render(request, 'situacionesadms/listado_reintegros_entrantes.html', context)