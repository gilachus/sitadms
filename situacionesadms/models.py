from django.db import models
from django.core.validators import FileExtensionValidator
from functools import partial
from django.conf import settings
from django.template.defaultfilters import slugify
from users.models import Empleado
from django.contrib.auth.models import User
# from cuser.fields import CurrentUserField
from cuser.middleware import CuserMiddleware
from django.utils import timezone 
from datetime import datetime, date
from .funciones_extra import nombre_aleatorio, update_filename, delta_fechas#, file_cleanup
# -delete files-
#from django.db.models.signals import post_delete
# ---------------



## 
class SituacionAdministrativa(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True, null=True)
    dias_anticipacion = models.IntegerField(default=0)
    max_horas_mensuales = models.IntegerField(default=0)
    max_dias_otorgables = models.IntegerField(default=0)
    max_meses_otorgables = models.IntegerField(default=0)
    dias_reintegro = models.IntegerField(default=0)
    dias_prorroga = models.IntegerField(default=0)
    meses_prorroga = models.IntegerField(default=0)
    # -------control-----------------------------------------------------------------------------------
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificaion = models.DateTimeField(auto_now=True)
    # ultimo_usuario = CurrentUserField(add_only=True, related_name="ultimo_usuario", on_delete=models.SET_NULL)
    ultimo_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

    class Meta:
         verbose_name_plural = "Situaciones Administrativas"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        user = CuserMiddleware.get_user()
        if user.is_authenticated:
            self.ultimo_usuario = user
        super(SituacionAdministrativa, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.nombre


class Solicitud(models.Model):
    ## -----------------------------------choices-----------------------------------------------------
    ESTADO = [(0, "papelera"), (1, "trámite"), (2, "corregida_modificada"), (3, "aprobada"), (4, "revocada"), (5, "rechazada")]
    ASISTE = [(1, "Estudiante"), (2, "Asistente"), (2, "Ponente"), (3, "Conferencista"), (4, "Otro")]
    VICE = [(0,"sin destino"), (1, "Docencia"), (2, "Administrativa")]
    TIPO = [(0,"Solicitud"),(1,"Modificación"), (1, "Corrección")] 
    PERIODO = [(0, 'todo el día'), (1, 'mañana'), (2, 'tarde')]
    ## --------Básicos-----------------------------------------------------------------------------------
    situacion = models.ForeignKey(SituacionAdministrativa, on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.PositiveIntegerField(default=0, choices=TIPO)
    estado = models.PositiveIntegerField(default=1, choices=ESTADO)
    fecha_i = models.DateField('Fecha inicio')
    fecha_f = models.DateField('Fecha fin')
    periodo = models.PositiveIntegerField(default=0, choices=PERIODO)
    dias_permiso = models.PositiveIntegerField('No. días', null=True, blank=True)
    justificacion = models.TextField("Justificación", help_text="<em>Describa su solicitud</em>", null=True, blank=True)
    ## --------comisión permiso_laboral------------------------------------------------------------------
    resolucion_viaticos = models.CharField("No. Resolución (viáticos)", max_length=50, null=True, blank=True)
    nombre_del_evento = models.CharField(max_length=120, null=True, blank=True)
    ciudad = models.CharField(max_length=50, null=True, blank=True)
    pais = models.CharField('País', max_length=50, null=True, blank=True)
    asiste_en_calidad = models.PositiveIntegerField(choices=ASISTE, null=True, blank=True)
    ## -------Archivos-----------------------------------------------------------------------------------
    soportes = models.FileField(upload_to=partial(update_filename,path="attached"), null=True, blank=True, validators=[FileExtensionValidator(['docx','doc'])])
    convenio = models.FileField(upload_to=partial(update_filename,path="agreement"), null=True, blank=True, validators=[FileExtensionValidator(['docx','doc'])])
    ## -------encargo------------------------------------------------------------------------------------
    requiere_encargo = models.BooleanField(default=False)
    nombre_encargo = models.CharField("Nombre Funcionario", max_length=50, null=True, blank=True)
    apellido_encargo = models.CharField("Apellido Funcionario", max_length=50, null=True, blank=True)
    cargo_encargo = models.CharField("Cargo Funcionario", max_length=100, null=True, blank=True)
    ## -------disfrute y reservas -----------------------------------------------------------------------
    no_reserva_rectoria = models.CharField("No. reserva rectoría", max_length=20, null=True, blank=True, help_text='<em>¿la reserva viene de Rectoría?</em>') # dias reservado por rectoria
    no_reserva_personal = models.CharField("No. reserva personal", max_length=50, null=True, blank=True, help_text='<em>¿La reserva la solicitó usted?</em>')                         # dias reservado por la persona
    no_reserva_previa = models.ManyToManyField("Solicitud", blank=True, related_name='solicitud_reserva')                    # probando el manytomany para hacerlo automatico 
    resolucion_vaciones = models.CharField("No. resolución Vacaciones", max_length=20, null=True, blank=True)                         # No. resolucion sobre el periodo vacaciones                             
    no_dias_a_reservar = models.PositiveIntegerField("No. días a reservar", null=True, blank=True)       # dias a reservar
    no_dias_a_disfrutar = models.PositiveIntegerField("No. días a disfrutar", null=True, blank=True)     # dias a disfrutar compensatorio o vacaciones reservadas
    dias_pendientes1 = models.PositiveIntegerField("Días pendientes", null=True, blank=True)             # lo calculan en Asuntos Laborales
    dias_pendientes2 = models.PositiveIntegerField(null=True, blank=True)              # para probar algoritmo calcula dias_pendientes()
    ## -------control y modificación-----------------------------------------------------------------------------------
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    ultimo_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ## --------------------------------------------------------------------------------------------------------------
    requiere_reintegro = models.BooleanField(default=False)
    modifica_a = models.OneToOneField("Solicitud", on_delete=models.SET_NULL, null=True, blank=True) # "edita"
    fue_modificada = models.BooleanField(default=False)
    extiende_a = models.OneToOneField("Solicitud", on_delete=models.SET_NULL, null=True, blank=True, related_name="extiende")
    ## -------revisar-----------------------------------------------------------------------------------
    revisar_planeacion = models.BooleanField(default=False)
    revisar_perfil = models.BooleanField(default=True)
    ## -------checks------------------------------------------------------------------------------------ 
    va_a_vice = models.PositiveIntegerField(choices=VICE, null=True, blank=True)
    check_jefe_inmediato = models.BooleanField(default=False)
    check_asistente_OAGHDP = models.BooleanField(default=False)  # primera revisión 
    check_asistente2_OAGHDP = models.BooleanField(default=False) # sabaticos y comisiones > 6 meses - convenios
    check_asistente_AL = models.BooleanField(default=False)  # revisa disfrute de vaciones
    check_jefe_AL = models.BooleanField(default=False)       # aprueba disfrute de vaciones
    check_abogado_AL = models.BooleanField(default=False)     # licencia incapacidad, maternidad, paternindad, luto
    check_jefe_OAGHDP = models.BooleanField(default=False)       # revisa todo
    check_planeacion = models.BooleanField(default=False)    # horarios profesores
    check_seleccion = models.BooleanField(default=False)     # caso de encargo
    check_vice_doc = models.BooleanField(default=False)      # se da por notificado
    check_vice_adm = models.BooleanField(default=False)      # se da por notificado
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
         verbose_name_plural = "Solicitudes"

    def dias_pendientes(self):
        pass

    def total_dias(self):
        delta_fecha_dias = self.fecha_f - self.fecha_i
        return delta_fecha_dias.days+1

    def __str__(self):
        return str(self.id)

    ## modificable
    def modificable_corregible(self):
        """ver si la situación ya debio utilizarse para permitir las modificaciones
        y correcciones"""
        if self.fecha_i >= date.today():
            return True
        else:
            return False

    ## comparar fecha creacion y actualizacion para ver si fue modificada
    def modificada(self):
        pass
    
    def reintegro_vencido(self):
        ## datetime_object = datetime.strptime("16/09/2019", "%d/%m/%Y")
        if delta_fechas(self.fecha_f, date.today())<1:
            if self.reintegro_set.all().count():
                return "OK"
            else:
                return "falta reintegro"
        return "en proceso"
    
    def nombre_situacion(self):
        nombre = self.situacion.nombre
        return f'{nombre}'

    def tiene_reintegro(self):
        consulta = self.reintegro_set.all()
        for reintegro in consulta:
            if check_jefe_OAGHDP:
                return True
        else:
            return False

    # def save(self):
    #     for field in self._meta.fields:
    #         if field.name == 'soportes':
    #             field.upload_to = 'attached/{}'.format(nombre_aleatorio(5))
    #     super(Solicitud, self).save()

# post_delete.connect(file_cleanup, sender=Image, dispatch_uid="gallery.image.file_cleanup")
      

class DetalleRechazo(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    motivo = models.TextField(help_text="<em>Describa las razones por las cual se rechaza</em>")
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    visto = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.solicitud)


class Encargo(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    funcionario_encargo = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)


class Reintegro(models.Model):
    SEGUIMIENTO = [(0, "papelera"), (1, "trámite"), (2, "corregida_modificada"), (3, "aprobada"), (4, "revocada"), (5, "rechazada")]
    situacion = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    cumplido = models.FileField(upload_to="cumplidos")
    pendiente_soporte = models.BooleanField(default=False)
    seguimiento = models.PositiveIntegerField(default=1, choices=SEGUIMIENTO)
    ## -------control-----------------------------------------------------------------------------------
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificaion = models.DateTimeField(auto_now=True)
    ## -------checks-----------------------------------------------------------------------------------
    check_asistente_OAGHDP = models.BooleanField(default=False)
    check_jefe_OAGHDP = models.BooleanField(default=False)

    def __str__(self):
        return "(R) {}".format(self.situacion)

class CartaEstemporaneo(models.Model):
    reintegro = models.ForeignKey(Reintegro, on_delete=models.CASCADE)
    redaccion = models.TextField()
    visto = models.BooleanField(default=False)
    def __str__(self):
        return "reintegro-estemporaneo: {}".format(self.reintegro.id)


## opción a futuro
class TipoResolucion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
         verbose_name_plural = "Tipo Resoluciones"

    def __str__(self):
        return self.nombre


class Resolucion(models.Model):
    tipo = models.ForeignKey(TipoResolucion, on_delete=models.SET_NULL, null=True, blank=True)
    numero = models.CharField(max_length=50, unique=True)
    fecha = models.DateField()
    documento = models.FileField(upload_to="resolutions", null=True, blank=True)
    fecha_update = models.DateTimeField(auto_now=True)
    
    class Meta:
         verbose_name_plural = "Resoluciones"

    def __str__(self):
        return self.nombre

    
