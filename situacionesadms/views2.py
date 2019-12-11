from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Solicitud
from .forms import ReintegroForm

# views para los reintegros
def llenar_reintegro(request, id_solicitud):
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