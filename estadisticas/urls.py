from .views import estadistica
from django.urls import path

app_name = 'estadistica'

urlpatterns = [
    path('estadisticas/', estadictica, name="estadicticas"),
]