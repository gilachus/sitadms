from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# class RegistroFormv2(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]

class RegistroFormV1(UserCreationForm):
    class Meta:
            model = User
            fields = ["username", "password1", "password2"]
            labels = {
                'username': 'Cédula:',
            }
            
    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     if not data.isdigit():
    #         raise forms.ValidationError("la cédula solo debe contener números")
    #     return data
    # def clean(self):
    #     cleaned_data = super().clean()
    #     data = cleaned_data.get("username")
    #     if data.isdigit():
    #         msg = "La cédula solo debe contener dígitos"
    #         self.add_error('username', msg)
          

class EntrarForm(AuthenticationForm):
    # username = forms.CharField(max_length=50, widget=forms.NumberInput())
    username = forms.CharField(label="Cédula", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'CC', 'autocomplete':'off', 'type':'number'}))
    password = forms.CharField(label="Contraseña", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'contraseña'}))
    class Meta:
        model = User
        fields = ["username", "password"]
    
    # def confirm_login_allowed(self, user):
    #     if not user.is_active:
    #         raise forms.ValidationError("usuario o contraseña incorrecta")

    def clean(self):
        username = self.cleaned_data.get("username")
        user = User.objects.all().filter(username=username).first()
        if user:
            if user.is_superuser and not user.is_active:
                msg = "credenciales incorrectas*"
                raise forms.ValidationError(msg)
                #self.add_error('username', msg)
            elif not user.is_active:
                msg = "credenciales incorrectas**"
                raise forms.ValidationError(msg)
            else:
                super().clean()
        else:
            msg = "credenciales incorrectas***"
            raise forms.ValidationError(msg)
        