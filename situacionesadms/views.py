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
                    RechazoForm) 
from .disabled_forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .funciones_extra import valida_empleado, valida_acceso, ESTADO, notas_situacion
from django.db.models import Q


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
def retorna_form(slug):
    """retorna un form dependiendo de la situacion adm que quiere diligenciar el usuario"""

    dict_forms = {"permiso-remunerado": PermisoRemuneradoForm,
                "permiso-sindical": JustificacionYEncargoForm,
                "permiso-laboral": PermisoLaboralForm,
                "comision-de-servicio": ComisionForm,
                "comision-de-estudio-menor-6-meses": ComisionForm,
                "comision-de-estudio-mayor-6-meses": ComisionForm,
                "comision-menor-a-15-dias-viaticos": ComisionViaticosForm,
                "permiso-academico-compensado-interno": JustificacionYEncargoForm,
                "permiso-academico-compensado-externo": JustificacionYEncargoForm,
                "permiso-para-ejercer-docencia-universitaria": JustificacionYEncargoForm,
                "licencia-especial-para-docentes": BasicForm,
                "licencia-ordinaria-no-remunerada": BasicForm,
                "licencia-no-remunerada-para-adelantar-estudios": BasicForm,
                "reserva-de-vacaciones": ReservaVacacionesForm,
                "disfrute-de-vacaciones-reservadas": DisfruteVacacionesForm,
                "reserva-de-dias-compensatorios": ReservaCompensatorio,
                "disfrute-de-dias-compensatorios": DisfruteCompensatorio,
                "licencia-por-enfermedad": ConEncargoForm,
                "licencia-por-maternidad": ConEncargoForm,
                "licencia-por-paternidad": ConEncargoForm,
                "licencia-por-luto": ConEncargoForm,
                "licencia-deportiva":JustificacionYEncargoForm,
                }
    if slug in dict_forms:
        return dict_forms[slug]
    else:
        return BasicForm
    

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
    ## Vacaciones
    if user.empleado.tipo_acceso == 6: 
        solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
        Q(situacion__nombre="disfrute de vacaciones reservadas"), Q(check_asistente_al=True))
    
    ## luto enfermedad paternidad maternidad 
    elif user.empleado.tipo_acceso==5:
        solicitudes = base.filter(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
        Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto")).exclude(Q(check_abogado_AL=True))

    ## Jefe Vacaciones
    elif user.empleado.tipo_acceso == 7:
        solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
        Q(situacion__nombre="reserva de vacaciones"), Q(check_asistente_AL=True) & Q(check_jefe_AL=False))

    ## Asistente OAGHDP
    elif user.empleado.tipo_acceso == 2:
        solicitudes = base.exclude(Q(situacion__nombre="reserva de vacaciones") | Q(situacion__nombre="disfrute de vacaciones reservadas") , 
        Q(check_jefe_AL=False) & Q(check_jefe_AL=False)).exclude(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
        Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto"), Q(check_abogado_AL=False))
        
    ## Jefe OAGHDP
    elif user.empleado.tipo_acceso == 4:
        solicitudes = base.filter(Q(check_asistente_OAGHDP), Q(requiere_estudio_perfil=True) & Q(check_seleccion=True))
    ## vice doc
    elif user.empleado.tipo_acceso == 10:
        solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & q(va_a_vice=1))
    ## vice adm
    elif user.empleado.tipo_acceso == 11:
        solicitudes = base.filter(Q(check_jefe_OAGHDP=True) & q(va_a_vice=2))
    
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
    print(solicitud.situacion.nombre)
    forms = retorna_disabled_form(solicitud.situacion.slug)
    form = forms(instance=solicitud)
    context = {
        'solicitud': solicitud,
        'form': form
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
            print(request.POST.get('motivo'))
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
    elif accesoo == 5:
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
## ----sección reintegro

## ----situaciones interno sección sabático - comision mayor 6 meses----
@login_required
def selecciona_interno(request):
    if not valida_empleado(request):
        return redirect('users:inicio')
    if request.method == 'POST':
        pass
        #TODO buscar funcionarios
    context = {}
    return render(request, 'situacionesadms/selecciona_interno.html', context)


@login_required
def formato_interno(request, slug_interno):
    if not valida_empleado(request):
        return redirect('users:inicio')
    situacion = get_object_or_404(SituacionAdministrativa, slug=slug_interno)
    if request.method == 'POST':
        forms = retorna_form(slug_interno)
        form = forms(request.POST, request.FILES)
        empleado_form = EmpleadoForm(request.POST)
    return render(request, 'situacionesadms:formato_interno')

@login_required
def listado_interno(request):
    pass

## ---------------------------------------------------------------------------------------------
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