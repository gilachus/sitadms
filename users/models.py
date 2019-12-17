from django.db import models
from django.contrib.auth.models import User

class TipoVinculacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class SedeDependencia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model): # asistente_2 -> sabaticos y comisiones > 6 meses
    ACCESO = [(1, "simple"), (2, "asistente_OAGHDP"), (3, "asistente2_OAGHDP"), (4, "jefe_OAGHDP"), 
    (5, "abogado_AL"), (6, "vacaciones_AL"), (7, "jefe_AL"), (8, "seleccion"), 
    (9, "planeacion"), (10, "vice_doc"), (11, "vice_adm"), (12, "comunicacion_AL")]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_vinculacion = models.ForeignKey(TipoVinculacion, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    jefe_inmediato = models.ForeignKey("Empleado", on_delete=models.SET_NULL, null=True, blank=True)
    sede_dependencia = models.ForeignKey(SedeDependencia, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_acceso = models.IntegerField(default=1, choices=ACCESO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ('user.name', '-fecha_creacion')
    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios' 

    def __str__(self):
        return self.user.username
    
    def nombre_completo(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def activo(self):
        return self.user.is_active
