from .views import (selecciona, llenar_formato, mis_solicitudes, modifica_corrige_a,
    solicitudes_entrantes, revision_solicitud, aceptar, rechazar, requiere_estudio_perfil,
    selecciona_interno, formato_interno, listado_interno, editar_interno,
    llenar_tipos_situaciones)
from django.urls import path
from django.core.exceptions import PermissionDenied
from .views import selectdate
from .views2 import (llenar_reintegro, reintegros_entrantes)

app_name = 'situacionesadms'

urlpatterns = [
    ## funcionarios
    path('selecciona/', selecciona, name="selecciona"),
    path('formato/<slug:slug>/', llenar_formato, name="formato"),
    path('mis_solicitudes/', mis_solicitudes, name="mis_solicitudes"),
        ## funcionario modifica o corrige
    path('cambio/<slug:accion>/<int:id_solicitud>/', modifica_corrige_a, name="modifica_corrige_a"),
        ## reintegros----------------------------------------------------------------------------
    path('llenar_reintegro/<int:id_solicitud>/', llenar_reintegro, name="llenar_reintegro"),

    ## revisiones
    path('solicitudes_entrantes/', solicitudes_entrantes, name="solicitudes_entrantes"),
    path('revision_solicitud/<int:solicitud_id>/', revision_solicitud, name="revision_solicitud"),
    path('rechazar/<int:id_solicitud>/', rechazar, name="rechazar"),
    path('aceptar/<int:id_solicitud>/', aceptar, name="aceptar"),
    path('requiere_estudio_perfil/<int:id_solicitud>/', requiere_estudio_perfil, name="requiere_estudio_perfil"),
        ## reintegros 
    path('reintegros_entrantes/', reintegros_entrantes, name="reintegros_entrantes"),

    ## interno
    path('selecciona_interno/', selecciona_interno, name="selecciona_interno"),
    path('formato_interno/<slug:slug_interno>/funcionario/<int:pk>/', formato_interno, name="formato_interno"),
    path('listado_interno/', listado_interno, name="listado_interno"),
    path('editar_interno/<slug:slug_interno>/<int:id_solicitud_interno>/', editar_interno, name="editar_interno"),

    ## función para lenar bases
    path('llenar/', llenar_tipos_situaciones, name="llenar"),

    ##probando código
    path('selectdate', selectdate, name="selectdate")
]