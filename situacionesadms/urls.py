from .views import (selecciona, formato, llenar_tipos_situaciones, mis_solicitudes, 
                    solicitudes_entrantes, revision_solicitud, aceptar, rechazar, selecciona_interno, formato_interno)
from django.urls import path
from django.core.exceptions import PermissionDenied

app_name = 'situacionesadms'

urlpatterns = [
    path('selecciona/', selecciona, name="selecciona"),
    path('formato/<slug:slug>/', formato, name="formato"),
    path('mis_solicitudes/', mis_solicitudes, name="mis_solicitudes"),
    # path('formato/permiso_remunerado/', permiso_remunerado, name='permiso_remunerado'),
    ## revisiones
    path('solicitudes_entrantes/', solicitudes_entrantes, name="solicitudes_entrantes"),
    path('revision_solicitud/<int:id>/', revision_solicitud, name="revision_solicitud"),
    path('aceptar/', aceptar, name="aceptar"),
    path('rechazar/<int:id_solicitud>', rechazar, name="rechazar"),
    ## OAGHDP
    path('selecciona_interno/', selecciona_interno, name="selecciona_interno"),
    path('formato_interno/<slug:slug>', formato_interno, name="formato_interno"),
    ## función para lenar bases
    path('llenar/', llenar_tipos_situaciones, name="llenar"),
]