from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import string
import random
from .models import Empleado
from .forms import EntrarForm #, RegistroFormV1 
from .lista import list # por si quiero restringir los registros
from situacionesadms.funciones_extra import valida_empleado 


@login_required
def inicio(request):
    """Página de inicio"""
    if not valida_empleado(request):
        messages.error(request, 'cuenta de funcionario incompleta') # funcionario==empleado
    permisos_interno = [2,3,4]
    context={'permisos_interno':permisos_interno}
    return render(request, 'users/inicio.html', context)


def registro(request):
    """Registro usuario nuevo"""
    lista = list
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            if username in lista :
                if username.isdigit():
                    user = form.save(commit=False)
                    user.save()
                    # try:
                    #     empleado = Empleado.objects.create(user=user)
                    # except Exception as e:
                    #     messages.error(request, "error al crear empleado. "+repr(e))
                    print(form.cleaned_data.get('username'))
                    print(form.cleaned_data.get('password1'))
                    messages.success(request, 'usuario creado')
                    
                else:
                    messages.error(request, 'formato de cédula incorrecto')
            else:
                messages.error(request, 'usuario no autorizado')
    else:
        form = UserCreationForm() 
    context = {
        'form': form
    }
    return render(request, 'users/registro.html', context)


def entrar(request):
    """iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('users:inicio')
    if request.method == 'POST':
        form = EntrarForm(data=request.POST) # (data = request.POST)
        data = request.POST.copy() 
        if form.is_valid():
            if data.get('username').isdigit():
                user = form.get_user()
                login(request, user)
                return redirect('users:inicio')
            else:
                messages.error(request, 'formato de cédula incorrecto')
    else:
        form = EntrarForm()
    context = {
        'form': form
    }
    return render(request, 'users/entrar.html', context)


def perfil(request):
    """datos del empleado"""
    if not valida_empleado(request):
        return redirect('users:inicio')
    user = User.objects.filter(username=request.user.username).first()
    context = {
        'user': user
    }
    return render(request, 'users/perfil.html', context)


@login_required
def csvloader(request):
    """cargar archivo csv de los empleados"""
    data = {}
    if request.method == "GET":
        return render(request, "users/csvloader.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'El archivo no es de tipo csv')
            return HttpResponseRedirect(reverse("users:csvloader"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"El archivo es muy grande (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("users:csvloader"))

        file_data = csv_file.read().decode("utf-8")		
        lines = file_data.split("\n")
        if 1 == int(request.POST['modelo']):
            #loop over the lines and save them in db. If error , store as string and then display
            for line in lines:						
                fields = line.split(";")
                data_dict = {}
                data_dict["username"] = fields[0] # cédula
                data_dict["first_name"] = fields[1]
                data_dict["last_name"] = fields[2]
                data_dict["email"] = fields[3]
                print(data_dict)
                letters = string.ascii_lowercase + string.digits
                password=''.join(random.choice(letters) for i in range(8))
                print(password)
                try: 
                    user = User.objects.create_user(
                        fields[0],
                        fields[3],
                        password)
                    try:
                        empleado = Empleado.objects.create(user=user, tipo_de_acceso=1)
                    except Exception as e:
                        messages.error(request, "error al crear empleado. "+repr(e))
                except Exception as e:
                    messages.error(request,"Error creando"+repr(e))
        elif 2 == int(request.POST['modelo']):   
            messages.error(request, "funcion en construcción")
            # TODO cargar cargos, sede/dependencia y vinculación
    except Exception as e:
        messages.error(request,"Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("users:csvloader"))


