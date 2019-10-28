from django.contrib import admin
from .models import TipoResolucion, Resolucion, SituacionAdministrativa, Solicitud, Reintegro, DetalleRechazo


class SituacionAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'ultimo_usuario', 'slug']
    list_display_links = ['__str__']
    class Meta:
        model = SituacionAdministrativa


class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'situacion', 'empleado', 'estado', 'fecha_i', 'fecha_f', 'fecha_creacion']
    list_display_links = ['situacion']
    list_filter = ['situacion']
    search_fields = ['empleado']
    # date_hierarchy = 'fecha_creacion'
    class Meta:
        model = Solicitud


admin.site.register(TipoResolucion)
admin.site.register(Resolucion)
admin.site.register(SituacionAdministrativa, SituacionAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Reintegro)
admin.site.register(DetalleRechazo)
# commit?
