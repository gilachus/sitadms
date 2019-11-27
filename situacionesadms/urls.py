from .views import (selecciona, formato, mis_solicitudes, 
                    solicitudes_entrantes, revision_solicitud, aceptar, rechazar, requiere_estudio_perfil,
                    selecciona_interno, formato_interno, listado_interno, editar_interno,
                    llenar_tipos_situaciones)
from django.urls import path
from django.core.exceptions import PermissionDenied
from .views import selectdate

app_name = 'situacionesadms'

urlpatterns = [
    ## funcionarios
    path('selecciona/', selecciona, name="selecciona"),
    path('formato/<slug:slug>/', formato, name="formato"),
    path('mis_solicitudes/', mis_solicitudes, name="mis_solicitudes"),
    ## revisiones
    path('solicitudes_entrantes/', solicitudes_entrantes, name="solicitudes_entrantes"),
    path('revision_solicitud/<int:solicitud_id>/', revision_solicitud, name="revision_solicitud"),
    path('rechazar/<int:id_solicitud>', rechazar, name="rechazar"),
    path('aceptar/<int:id_solicitud>', aceptar, name="aceptar"),
    path('requiere_estudio_perfil/<int:id_solicitud>', requiere_estudio_perfil, name="requiere_estudio_perfil"),
    ## interno
    path('selecciona_interno/', selecciona_interno, name="selecciona_interno"),
    path('formato_interno/<slug:slug_interno>/funcionario/<int:pk>', formato_interno, name="formato_interno"),
    path('listado_interno', listado_interno, name="listado_interno"),
    path('editar_interno/<slug:slug_interno>/<int:id_solicitud_interno>', editar_interno, name="editar_interno"),
    ## función para lenar bases
    path('llenar/', llenar_tipos_situaciones, name="llenar"),

    ##probando código
    path('selectdate', selectdate, name="selectdate")
]