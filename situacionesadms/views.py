import os
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.paginator import Paginator #, EmptyPage, PageNotAnInteger
from .models import SituacionAdministrativa, Solicitud
from users.models import Empleado, TipoVinculacion
from django.utils import timezone
from .forms import (BasicForm, ConJustificacionForm, ConEncargoForm, JustificacionYEncargoForm, 
                    PermisoRemuneradoForm, PermisoLaboralForm, ComisionForm, ComisionViaticosForm, 
                    ReservaVacacionesForm, DisfruteVacacionesForm, 
                    ReservaCompensatorio, DisfruteCompensatorio,
                    RechazoForm, ComisionMayorSeisSabaticoFormEdit) 
from .disabled_forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .funciones_extra import valida_empleado, valida_acceso, ESTADO, notas_situacion
from django.db.models import Q
from .utils import retorna_form
from .forms import SelectdateForm


## sección usuario básico
@login_required
def selecciona(request):
    """ seleccionar el tipo de situación a diligenciar"""
    if not valida_empleado(request):
        return redirect('users:inicio')
        
    situaciones = SituacionAdministrativa.objects.all().exclude(Q(nombre="año sabático") | 
    Q(nombre="comisión de estudio mayor 6 meses"))

    context = {
        'situaciones': situaciones
    }
    return render(request, 'situacionesadms/selecciona_situaciones.html', context)


### selecciona fomato.txt

### retorna_template.txt

## guardar formato de situacion administrativa 
@login_required
def formato(request, slug):
    """método donde se llenan y guardan los datos de la situacion adm solicitada"""
    if not valida_empleado(request):
        return redirect('users:inicio')
    situacion = get_object_or_404(SituacionAdministrativa, slug=slug)
    empleado = get_object_or_404(Empleado, user=request.user)
    if request.method == 'POST':
        forms = retorna_form(slug)
        form = forms(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.situacion = situacion
            solicitud.empleado = empleado
            solicitud.save()
            messages.success(request, 'Solicitud enviada')
            return redirect('users:inicio')
        else:
            messages.error(request, 'error en formulario')
    else:       
        forms = retorna_form(slug)
        form = forms()
    fecha = timezone.now()
    solicitud = slug.replace("-", " ")
    template = "situacionesadms/formato.html"
    nota_situacion = notas_situacion(slug)
    context = {
        'fecha': fecha,
        'solicitud': solicitud,
        'form': form,
        'nota_situacion': nota_situacion
    }
    return render(request, template, context)


## 001.txt
@login_required()
def mis_solicitudes(request):
    """ver listado de solicitudes personales"""
    if not valida_empleado(request):
        return redirect('users:inicio')
    user = request.user
    solicitudes = Solicitud.objects.filter(empleado=user.empleado).exclude(estado=0).order_by('-fecha_creacion')
    estados = ESTADO
    paginator = Paginator(solicitudes, 5)
    page = request.GET.get('page') ## ?page=2
    if page:
        solicitudes = paginator.get_page(page)
    else:
        page=1
        solicitudes = paginator.get_page(page)
    context = {
        'solicitudes': solicitudes,
        'estados': estados,
        'page': page
    }
    return render(request, 'situacionesadms/mis_solicitudes.html', context)


def modifica_corrige_a(request, accion, id_solicitud):
    ## opcion clonar
    # hero = Hero.objects.first()
    # hero.pk = None
    # hero.save()
    solicitud_nueva = get_object_or_404(Solicitud, pk=id_solicitud)
    slug_situacion = solicitud_nueva.situacion.slug
    if slug_situacion:
        print(slug_situacion)
        forms = retorna_form(slug_situacion)
    else: 
        messages.error(request, "error: la solicitud no tiene un tipo de situación definido")
        return redirect('situacionesadms:mis_solicitudes')
    solicitud_nueva.pk = None #clonando
    if request.method == 'POST':
        form = forms(request.POST, request.FILES)
        if form.is_valid:
            vieja=get_object_or_404(Solicitud, pk=id_solicitud)
            nueva = form.save(commit=False)
            nueva.tipo=1
            # nueva.modifica_a=vieja
            # nueva.situacion=vieja.situacion
            # nueva.empleado=vieja.empleado
            # nueva.soportes=vieja.soportes
            nueva.save()
            print(accion)
            return redirect('situacionesadms:mis_solicitudes')
    else:
        form=forms(instance=solicitud_nueva)
    context = {
        'form': form,
        'accion': accion,
        'solicitud_actual': id_solicitud,
        'solicitud_nueva': solicitud_nueva,
    }
    return render(request, 'situacionesadms/modifica_corrige_a.html', context)



## ---------------------------------------------------------------------------
## ----------------------sección gestión--------------------------------------

@login_required
def solicitudes_entrantes(request):
    """Dependiento el perfil del usuario se mostrara un listado"""
    if not valida_empleado(request):
        if not valida_acceso(request):
            return redirect('users:inicio')
    user = request.user
    estados = ESTADO
    base = Solicitud.objects.all().filter(estado=1)
    solicitudes = None
    
    if request.user.is_superuser:
        solicitudes = base

    ## revision luto enfermedad paternidad maternidad 
    elif user.empleado.tipo_acceso==5:
        solicitudes = base.filter(Q(situacion__nombre="licencia por enfermedad") | 
        Q(situacion__nombre="licencia por maternidad") | Q(situacion__nombre="licencia por paternidad") | 
        Q(situacion__nombre="licencia por luto")).exclude(Q(check_abogado_AL=True))
    
    ## revision Vacaciones
    elif user.empleado.tipo_acceso == 6: 
        solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
        Q(situacion__nombre="disfrute de vacaciones reservadas")).exclude(Q(check_asistente_al=True))
        
    ## Jefe al vaciones y abogado
    elif user.empleado.tipo_acceso == 7:
        solicitudes = base.filter((Q(check_asistente_AL=True) | Q(check_abogado_AL=True)) & Q(check_jefe_AL=False) #creo que se puede resumir así
            #(Q(situacion__nombre="reserva de vacaciones") | Q(situacion__nombre="reserva de vacaciones")) & 
            #(Q(check_asistente_AL=True) & Q(check_jefe_AL=False)) | 
            #(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
            #Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto")) & 
            #(Q(check_abogado_AL=True) & Q(check_jefe_AL=False))
            )

    ## revision Asistente OAGHDP
    elif user.empleado.tipo_acceso == 2:
        solicitudes = base.exclude(Q(situacion__nombre="reserva de vacaciones") | Q(situacion__nombre="disfrute de vacaciones reservadas") , 
        Q(check_jefe_AL=False) & Q(check_jefe_AL=False)).exclude(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
        Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto"), Q(check_abogado_AL=False))
        
    ## Jefe OAGHDP
    elif user.empleado.tipo_acceso == 4:
        solicitudes = base.filter(Q(check_asistente_OAGHDP=True) | Q(check_jefe_AL=True) | (Q(revisar_perfil=True) & Q(check_seleccion=True))) # 
    ## vice doc
    elif user.empleado.tipo_acceso == 10:
        solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & Q(va_a_vice=1))
    ## vice adm
    elif user.empleado.tipo_acceso == 11:
        solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & Q(va_a_vice=2))
    
    context = {
        'solicitudes': solicitudes.order_by('-fecha_creacion'),
        'estados': estados,
    }
    return render(request, 'situacionesadms/solicitudes_entrantes.html', context)


@login_required
def revision_solicitud(request, solicitud_id):
    if not valida_empleado(request):
        if not valida_acceso(request):
            return redirect('users:inicio')
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    if solicitud.soportes:
        nombre_soportes = os.path.basename(solicitud.soportes.file.name)
    if not solicitud.situacion:
        messages.error(request, "error solicitud: tipo de situacion administrativa no definida")
        return redirect('situacionesadms:solicitudes_entrantes')
    forms = retorna_disabled_form(solicitud.situacion.slug)
    form = forms(instance=solicitud)
    context = {
        'solicitud': solicitud,
        'form': form,
        'nombre_soportes': nombre_soportes
    }
    return render(request, 'situacionesadms/revision_solicitud.html', context)


@login_required
def rechazar(request,id_solicitud):
    """registrar solicitudes con errores"""
    if not valida_empleado(request):
        if not valida_acceso(request):
            return redirect('users:inicio')
    solicitud = get_object_or_404(Solicitud, pk=id_solicitud)
    form_solicitud = retorna_disabled_form(solicitud.situacion.slug)
    if request.method == 'POST':
        rechazo = RechazoForm(request.POST)
        if rechazo.is_valid:
            print("rechazado")
            instancia = rechazo.save(commit=False)
            instancia.solicitud = solicitud
            instancia.responsable = request.user
            instancia.save()
            solicitud.estado = 5 
            solicitud.save()
        return redirect('situacionesadms:solicitudes_entrantes')    
    context = {
        'solicitud': solicitud,
        'form_solicitud': form_solicitud(instance=solicitud),
        'form_rechazo': RechazoForm()
    }
    return render(request, 'situacionesadms/rechazar_solicitud.html', context)


@login_required
def aceptar(request, id_solicitud):
    if not valida_empleado(request):
        if not valida_acceso(request):
            return redirect('users:inicio')
    solicitud = get_object_or_404(Solicitud, pk=id_solicitud)
    acceso = request.user.empleado.acceso
    if acceso == 6:
        solicitud.check_asistente_AL = True
    elif acceso == 5:
        solicitud.check_abogado_AL = True
    elif acceso == 7:
        solicitud.check_jefe_AL = True
    elif acceso == 2:
        solicitud.check_asistente_OAGHDP = True
    elif acceso == 4:
        solicitud.user.check_jefe_OAGHDP = True
    elif acceso == 10:
        solicitud.user.check_vice_doc = True
        solicitud.estado = 3
    elif acceso == 11:
        solicitud.user.check_vice_adm = True
        solicitud.estado = 3

    solicitud.save()
    return redirect('situcionesadms:solicitudes_entrantes')
    

def requiere_estudio_perfil(self):
    pass


@login_required
def editar_solicitud(request, id):
    pass


## --------------------------------------------------------------------------------------------
## -------------sección reintegro--------------------------------------------------------------

## -------------extra reintegro----------------------------------------------------------------
def no_reintegro(id_solicitud):
    """poner que no requiere reintegro"""
    solicitud = Solicitud.get_object_or_404(id=id_solicitud)
    solicitud.requiere_reintegro = False
    solicitud.save()

def si_reintegro(id_solicitud):
    """poner que si requiere reintegro"""
    solicitud = Solicitud.get_object_or_404(id=id_solicitud)
    solicitud.requiere_reintegro = True
    solicitud.save()

## --------------------------------------------------------------------------------------
## ----situaciones interno sección comision mayor 6 meses - sabático---------------------

@login_required
def selecciona_interno(request):
    """primero buscar al funcionario y seleccionar el tipo de situacion administrativa(i)"""
    if not valida_empleado(request):
        return redirect('users:inicio')

    funcionarios=None
    if request.method == 'POST':
        consulta = request.POST.get('pista')
        if consulta:
            funcionarios = Empleado.objects.all().filter(Q(user__first_name__icontains=consulta) | Q(user__last_name__icontains=consulta))
        # funcionarios = Empleado.objects.all().filter(Q(nombre_completo__icontains="") & Q(activo=True))
    context = {
        'funcionarios': funcionarios,
    }
    print(funcionarios)
    return render(request, 'situacionesadms/selecciona_interno.html', context)


@login_required
def formato_interno(request, slug_interno, pk):
    """agregar soportes y convenio para el registro de la sistuacion administrativa(i)"""
    if not valida_empleado(request):
        return redirect('users:inicio')
    situacion = get_object_or_404(SituacionAdministrativa, slug=slug_interno)
    funcionario = get_object_or_404(Empleado, pk=pk)
    
    if request.method == 'POST':
        forms = retorna_form(slug_interno) 
        form = forms(request.POST, request.FILES)
        if form.is_valid:
            print("válido")
            formato = form.save(commit=False)
            formato.situacion = situacion
            formato.empleado = funcionario
            formato.estado = 3
            formato.save()
            messages.success(request, f"registro de -{situacion.nombre}- éxitoso ")
        return redirect('situacionesadms:selecciona_interno')
    else:
        forms = retorna_form(slug_interno) 
    context={
        'title': situacion.nombre,
        'form': forms(),
        'funcionario': funcionario,
        'slug': slug_interno 
    }
    return render(request, 'situacionesadms/formato_interno.html', context)

@login_required
def listado_interno(request):
    """listar situaciones administrativas(i)"""
    situaciones_interno = Solicitud.objects.all().filter(Q(situacion__nombre="comisión de estudio mayor 6 meses") | 
    Q(situacion__nombre="año sabático"))
    print(situaciones_interno)
    context = {
        'situaciones': situaciones_interno
    }
    return render(request, 'situacionesadms/listado_interno.html', context)

@login_required
def editar_interno(request, slug_interno, id_solicitud_interno):
    solicitud_interno = get_object_or_404(Solicitud, pk=id_solicitud_interno)
    #forms = retorna_form(slug_interno)
    forms = ComisionMayorSeisSabaticoFormEdit
    if request.method == 'POST':
        form = forms(request.POST, request.FILES)
        print('post...')
        if form.is_valid:
            form.save()
            messages.success(request, f"registro de -{solicitud_interno.situacion.nombre}- éxitoso ")
        return redirect('users:inicio')
    else:
        data={
            'fecha_i': solicitud_interno.fecha_i,
            'fecha_f': solicitud_interno.fecha_f,
            'soportes': solicitud_interno.soportes,
            'convenio': solicitud_interno.convenio
        }
        #form = forms(initial=data) 
        form = forms(instance=solicitud_interno)
    context = {
        'form': form,
        'title': solicitud_interno.situacion.nombre,
        'solicitud': solicitud_interno,
        'slug': slug_interno
    }
    return render(request, 'situacionesadms/editar_interno.html', context)

## ---------------------------------------------------------------------------------------------
## ----extra------------------------------------------------------------------------------------
@login_required
def llenar_tipos_situaciones(request):
    if request.user.is_superuser:
        situas = [
        "permiso remunerado", "permiso sindical", "permiso laboral", 
        "comisión de servicio", "comisión de estudio menor 6 meses", "comisión menor a 15 días viáticos", 
        "permiso académico compensado interno", "permiso académico compensado externo", 
        "permiso para ejercer docencia universitaria", "licencia especial para docentes", 
        "licencia ordinaria no remunerada", "licencia no remunerada para adelantar estudios", 
        "reserva de vacaciones", "disfrute de vacaciones reservadas", 
        "reserva de días compensatorios", "disfrute de días compensatorios", 
        "licencia por enfermedad", "licencia por maternidad", "licencia por paternidad", "licencia por luto", 
        "licencia deportiva", "año sabático", "comisión de estudio mayor 6 meses"]

        vinculacion = [
            "Empleado Público Docente", "Docente Ocasional", "Docente de Cátedra", 
        "Empleado Público no Docente", "Trabajador Oficial", "Contrato a Término Definido"]
        for situ in situas:
            obj1, created1 = SituacionAdministrativa.objects.get_or_create(nombre=situ)
        for vin in vinculacion:
            obj2, created2 = TipoVinculacion.objects.get_or_create(nombre=vin)
    return redirect('users:inicio')


@login_required
class DescargarArchivoView(View):
    def post(self, request, *args, **kwargs):
        try:
            solicitud = Solicitud.objects.get(pk=request.POST['id_solicitud'])
        except:
            messages.error("problemas con el archivo")
        response = HttpResponse(solicitud.soporte, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' % solicitud.soporte
        return response


##probando código...
def hacer_registro(self):
        fecha = datetime(int(self.data['fecha_de_nacimiento_year']),
                        int(self.data['fecha_de_nacimiento_month']),
                        int(self.data['fecha_de_nacimiento_day']))
        
        # nuevo_registro = Registro(nombre=self.data['nombre'],
        #                 fecha_de_nacimiento=fecha)
        # nuevo_regitro.save()
        return 'Registro exitoso'

def selectdate(request):
    if request.method == 'POST':
        form = SelectdateForm(request.POST)
        if register_form.is_valid():
            print('correcto')
            # success = register_form.registrar_usuario(request.user)
            # return redirect('./')
    else:
        form = SelectdateForm(initial={'fecha':'16/09/1990'})
        return render(request, 'situacionesadms/selectdate.html', {'form': form})
    