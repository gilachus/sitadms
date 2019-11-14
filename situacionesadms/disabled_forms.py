from django.forms import ModelForm
from .models import Solicitud
from django import forms

def retorna_disabled_form(slug):
    """retorna un form de campos desactivados"""
    dict_forms = {
        "permiso-remunerado": PermisoRemuneradoFormDisabled,
        "permiso-sindical": BasicFormDisabled,
        "permiso-laboral": BasicFormDisabled,
        "comision-de-servicio": ConJustificacionFormDisabled,
        "comision-de-estudio-menor-6-meses": BasicFormDisabled,
        "comision-de-estudio-mayor-6-meses": BasicFormDisabled,
        "comision-menor-a-15-dias-viaticos": BasicFormDisabled,
        "permiso-academico-compensado-interno": BasicFormDisabled,
        "permiso-academico-compensado-externo": BasicFormDisabled,
        "permiso-para-ejercer-docencia-universitaria": BasicFormDisabled,
        "licencia-especial-para-docentes": BasicFormDisabled,
        "licencia-ordinaria-no-remunerada": BasicFormDisabled,
        "licencia-no-remunerada-para-adelantar-estudios": BasicFormDisabled,
        "reserva-de-vacaciones": BasicFormDisabled,
        "disfrute-de-vacaciones-reservadas": BasicFormDisabled,
        "reserva-de-dias-compensatorios": BasicFormDisabled,
        "disfrute-de-dias-compensatorios": BasicFormDisabled,
        "licencia-por-enfermedad": BasicFormDisabled,
        "licencia-por-maternidad": BasicFormDisabled,
        "licencia por paternidad": BasicFormDisabled,
        "licencia por luto": BasicFormDisabled
                }
    if slug in dict_forms:
        return dict_forms[slug]
    else:
        return BasicFormDisabled


class BasicFormDisabled(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(BasicFormDisabled, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = ''
            
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control'}),
        }

class ConJustificacionFormDisabled(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(ConJustificacionFormDisabled, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = ''

    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': forms.DateInput(attrs={'class':'form-control'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'}),
        }

class ConEncargoFormDisabled(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(ConEncargoFormDisabled, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control'}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }


class JustificacionYEncargoFormDisabled(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(JustificacionYEncargoFormDisabled, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control'}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }


class PermisoRemuneradoFormDisabled(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(PermisoRemuneradoFormDisabled, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'dias_permiso', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': forms.DateInput(attrs={'class':'form-control'}),
            'fecha_f': forms.DateInput(attrs={'class':'form-control'}),
            'dias_permiso': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
        }