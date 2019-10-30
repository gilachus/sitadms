from .views import estadisticas, ultimos_encargos
from django.urls import path

app_name = 'estadisticas'

urlpatterns = [
    path('estadisticas/', estadisticas, name="estadisticas"),
    path('ultimos_encargos/', ultimos_encargos, name="ultimos_encargos"),
]