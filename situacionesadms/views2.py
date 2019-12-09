from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReintegroForm

# views para los reintegros
def llenar_reintegro(request):
    context = {
        'form': ReintegroForm(),
    }

    return render(request, 'situacionesadms/', context)