
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Empleado, SedeDependencia, Cargo, TipoVinculacion

admin.site.register(TipoVinculacion)
admin.site.register(SedeDependencia)
admin.site.register(Cargo)


class EmpleadoInline(admin.StackedInline):
    model = Empleado
    # can_delete = False
    verbose_name_plural = 'Empleados'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (EmpleadoInline, )
    
    # --------ejemplo de mostrar lo que devuelve un método (get_location)-----------------------
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
    # list_select_related = ('profile', )

    # def get_location(self, instance):
    #     return instance.profile.location
    # get_location.short_description = 'Location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_completo', 'tipo_vinculacion', 'cargo')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Empleado, EmpleadoAdmin)


