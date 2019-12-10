from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Solicitud
from .forms import ReintegroForm

# views para los reintegros
def llenar_reintegro(request, id_solicitud):
    situacion_objetivo = get_object_or_404(Solicitud, pk=id_solicitud)

    context = {
        'form': ReintegroForm(),
        'situacion_objetivo': situacion_objetivo
    }

    return render(request, 'situacionesadms/llenar_reintegro.html', context)