from django.contrib import admin
from .models import TipoResolucion, Resolucion, SituacionAdministrativa, Solicitud, Reintegro, DetalleRechazo


class SituacionAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'ultimo_usuario', 'slug']
    list_display_links = ['__str__']
    class Meta:
        model = SituacionAdministrativa


class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'situacion', 'empleado', 'estado', 'fecha_i', 'fecha_f', 'fecha_creacion']
    list_display_links = ['__str__']
    list_filter = ['situacion']
    search_fields = ['empleado__user__firstname','empleado__user__lastname','emplado__user__username']
    # date_hierarchy = 'fecha_creacion'

    ##--------------crear secciones dentro del admin form
    # fieldsets = (
    #     ('checks', {
    #         'fields': ('check_jefe_inmediato', 'check_asistente_OAGHDP')
    #     }),
    # )

    class Meta:
        model = Solicitud
    
    
admin.site.register(SituacionAdministrativa, SituacionAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Reintegro)
admin.site.register(DetalleRechazo)
# commit?

##---
admin.site.register(TipoResolucion)
admin.site.register(Resolucion)