from django.forms import ModelForm
from .models import Solicitud, DetalleRechazo
from django import forms


class BasicFormDisabled(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(BasicFormDisabled, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = ''
            
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }

class ConJustificacionFormDisabled(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(ConJustificacionFormDisabled, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = ''

    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'class':'form-control', 'autocomplete':'off'}),
            'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
        }