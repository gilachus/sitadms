from django.forms import ModelForm
from .models import Solicitud, DetalleRechazo
from django import forms

## para llenar el funcionario de los formatos internos
class EmpleadoForm(forms.Form):
    cedula = forms.CharField(label="Cédula Funcionario", max_length=30,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'CC', 
                            'autocomplete':'off', 'type':'number'}))


class BasicForm(ModelForm):
    # def __init__(self, *args, **kwargs): 
    #     super(BasicForm, self).__init__(*args, **kwargs)                       
    #     self.fields['__all__'].disabled = True

    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }


class ConJustificacionForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }
    

class ConEncargoForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }


class JustificacionYEncargoForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }


class PermisoRemuneradoForm(ModelForm):
    DIAS = [(1,"1"),(2,"2"),(3,"3")]
    dias_permiso = forms.ChoiceField(label="Días permiso" ,choices=DIAS)
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'dias_permiso', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
            'dias_permiso': forms.Select(attrs={'class':'form-control'}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }
        # labels = {
        #     'dias_permiso': 'Días permiso',
        # }


class PermisoLaboralForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'nombre_del_evento', 'ciudad', 'pais', 'asiste_en_calidad']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
            'nombre_del_evento': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'asiste_en_calidad': forms.Select(attrs={'class':'form-control'}),
        }


class ComisionForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes', 'nombre_del_evento', 'ciudad', 'pais', 'asiste_en_calidad', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
            'nombre_del_evento': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'pais': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'asiste_en_calidad': forms.Select(attrs={'class':'form-control'}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }


class ComisionViaticosForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'resolucion_viaticos', 'nombre_del_evento', 'ciudad', 'pais', 'asiste_en_calidad', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
            'resolucion_viaticos': forms.TextInput(attrs={'class':'form-control', 'type': 'number', 'min': '0', 'autocomplete':'off'}),
            'nombre_del_evento': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'pais': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'asiste_en_calidad': forms.Select(attrs={'class':'form-control'}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }    


class ReservaVacacionesForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['resolucion_vaciones', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            'resolucion_vaciones': forms.TextInput(attrs={'class':'form-control'}),
            'no_dias_a_reservar': forms.NumberInput(attrs={'class':'form-control'}),
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }


class DisfruteVacacionesForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_reserva_personal', 'no_dias_a_disfrutar', 'fecha_i', 'fecha_f', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'class':'form-control'}),
            'no_reserva_personal': forms.NumberInput(attrs={'class':'form-control'}),
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }


class DisfruteVacaciones2Form(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_reserva_personal', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'dias_pendientes1', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'no_reserva_personal': forms.NumberInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
        }


class ReservaCompensatorio(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'no_dias_a_reservar': forms.NumberInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'class':'form-control', 'autocomplete':'off'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }


class DisfruteCompensatorio(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_dias_a_disfrutar', 'fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'no_dias_a_disfrutar': forms.NumberInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'class':'form-control', 'autocomplete':'off'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }



## cambiando label
# class LaboralSindicalForm(ModelForm):        
#     class Meta:
#         model = Solicitud
#         fields = []

    ## método contructor ModelForms
    # def __init__(self, *args, **kwargs):
    #     super(RegistrationFormTOS, self).__init__(*args, **kwargs)
    #     self.fields['email'].label = "New Email Label"


## RECHAZO FORM
class RechazoForm(ModelForm):
    class Meta:
        model = DetalleRechazo
        fields = ['motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'})
        }


# Comisión Mayor Seis y Sabático
class ComisionMayorSeisSabaticoForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'convenio']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control'}),
            'soportes': forms.FileInput(attrs={'class':'form-control'}),
            'convenio': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }

class ComisionMayorSeisSabaticoFormEdit(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComisionMayorSeisSabaticoFormEdit, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'convenio']
        

