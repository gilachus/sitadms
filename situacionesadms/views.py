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


## seleccionar el tipo de situación a diligenciar
@login_required
def selecciona(request):
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
@login_required
def formato(request, slug):
    """lugar donde se llenan los datos de la situacion adm a solicitar"""
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
    
    ## Jefe Vacaciones
    elif user.empleado.tipo_acceso == 7:
        solicitudes = base.filter(Q(situacion__nombre="reserva de vacaciones") | 
        Q(situacion__nombre="reserva de vacaciones"), Q(check_asistente_AL=True) & Q(check_jefe_AL=False))
    
    ## luto enfermedad paternidad maternidad 
    elif user.empleado.tipo_acceso==5:
        solicitudes = base.filter(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
        Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto")).exclude(Q(check_licencias=True))

    ## Asistente OAGHDP
    elif user.empleado.tipo_acceso == 2:
        solicitudes = base.exclude(Q(situacion__nombre="reserva de vacaciones") | Q(situacion__nombre="disfrute de vacaciones reservadas") , 
        Q(check_jefe_AL=False) & Q(check_jefe_AL=False)).exclude(Q(situacion__nombre="licencia por enfermedad") | Q(situacion__nombre="licencia por maternidad") |
        Q(situacion__nombre="licencia por paternidad") | Q(situacion__nombre="licencia por luto"), Q(check_licencias=False))
        
    ## Jefe OAGHDP
    elif user.empleado.tipo_acceso == 4:
        solicitudes = base.filter(Q(check_asistente_OAGHDP), Q(requiere_estudio_perfil=True) & Q(check_seleccion=True))
    
    context = {
        'solicitudes': solicitudes.order_by('-fecha_creacion'),
        'estados': estados,
        }
    return render(request, 'situacionesadms/solicitudes_entrantes.html', context)


@login_required
def revision_solicitud(request, id):
    if not valida_empleado(request):
        return redirect('users:inicio')
    solicitud = get_object_or_404(Solicitud, id=id)
    context = {
        'solicitud': solicitud
    }
    return render(request, 'situacionesadms/revision_solicitud.html', context)

def retorna_disabled_form(slug):
    """retorna un form de campos desactivados"""

    dict_forms = {"permiso-remunerado": BasicFormDisabled,
                "permiso-sindical": BasicFormDisabled,
                "permiso-laboral": BasicFormDisabled,
                "comision-de-servicio": BasicFormDisabled,
                "comision-de-estudio-menor-6-meses": BasicFormDisabled,
                "comision-de-estudio-mayor-6-meses": BasicFormDisabled,
                "comision-menor-a-15-dias-viaticos": BasicFormDisabled,
                "permiso-academico-compensado-interno": BasicFormDisabled,
                "permiso-academico-compensado-externo": BasicFormDisabled,
                "permiso-para-ejercer-docencia-universitaria": BasicFormDisabled,
                "licencia-especial-para-docentes": BasicFormDisabled,
                "licencia-ordinaria-no-remunerada": BasicFormDisabled,
                "licencia-no-remunerada-para-adelantar-estudios": BasicFormDisabled,
                "reserva-de-vacaciones": BasicFormDisabled,
                "disfrute-de-vacaciones-reservadas": BasicFormDisabled,
                "reserva-de-dias-compensatorios": BasicFormDisabled,
                "disfrute-de-dias-compensatorios": BasicFormDisabled,
                "licencia-por-enfermedad": BasicFormDisabled,
                "licencia-por-maternidad": BasicFormDisabled,
                "licencia por paternidad": BasicFormDisabled,
                "licencia por luto": BasicFormDisabled
                }
    if slug in dict_forms:
        return dict_forms[slug]
    else:
        return BasicFormDisabled

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
    if request.user.empleadp.acceso == 2:
        pass

    return redirect('situcionesadms:')
    
def requiere_estudio_perfil(self):
    pass


@login_required
def editar_solicitud(request, id):
    pass


## ----sabático - comision mayor 6 meses----
@login_required
def selecciona_interno(request):
    if not valida_empleado(request):
        return redirect('users:inicio')
    context = {}
    return render(request, 'situacionesadms/selecciona_interno.html', context)


@login_required
def formato_interno(request, slug):
    if not valida_empleado(request):
        return redirect('users:inicio')
    situacion = get_object_or_404(SituacionAdministrativa, slug=slug)
    if request.method == 'POST':
        forms = retorna_form(slug)
        form = forms(request.POST, request.FILES)
        empleado_form = EmpleadoForm(request.POST)
    return render(request, 'situacionesadms:formato_interno')


## ----extra------------------------------------------------------------------------------------
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
        "licencia deportiva", "modificación", "año sabático", "comisión de estudio mayor 6 meses"]

        vinculacion = [
            "Empleado Público Docente", "Docente Ocasional", "Docente de Cátedra", 
        "Empleado Público no Docente", "Trabajador Oficial", "Contrato a Término Definido"]
        for situ in situas:
            obj1, created1 = SituacionAdministrativa.objects.get_or_create(nombre=situ)
        for vin in vinculacion:
            obj2, created2 = TipoVinculacion.objects.get_or_create(nombre=vin)
    return redirect('users:inicio')