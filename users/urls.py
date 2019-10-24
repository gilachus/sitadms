from django.urls import path
from django.contrib.auth import views as auth_view
# from django.contrib.auth.forms import AuthenticationForm

from .views import registro, inicio, entrar, csvloader, perfil

app_name = 'users'

urlpatterns = [
    path('inicio/', inicio, name='inicio'),
    # path('entrar/', auth_view.LoginView.as_view(template_name='users/entrar.html', authentication_form=AuthenticationForm), name='entrar'),
    path('entrar/', entrar, name='entrar'),
    path('cerrar/', auth_view.LogoutView.as_view(template_name='users/entrar.html'), name='cerrar'),
    path('perfil/', perfil, name='perfil'),
    # path('registro/', registro, name='registro'),
    path('csvloader/', csvloader, name='csvloader'),
]