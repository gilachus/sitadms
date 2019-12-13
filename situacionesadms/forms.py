from django.forms import ModelForm
from .models import Solicitud, DetalleRechazo, Reintegro
from django import forms

# para colocar type date alos inputs
class DateInput2(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


## para llenar el funcionario de los formatos internos
class EmpleadoForm(forms.Form):
    cedula = forms.CharField(label="Cédula Funcionario", max_length=30,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'CC', 
                            'autocomplete':'off', 'type':'number'}))


class BasicForm(ModelForm):
    # def __init__(self, *args, **kwargs): 
    #     super(BasicForm, self).__init__(*args, **kwargs)                       
    #     self.fields['__all__'].disabled = True
    def __init__(self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2()
        }


class ConJustificacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConJustificacionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
        }
    

class ConEncargoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConEncargoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }


class JustificacionYEncargoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(JustificacionYEncargoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }


class PermisoRemuneradoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermisoRemuneradoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    DIAS = [(1,"1"),(2,"2"),(3,"3")]
    dias_permiso = forms.ChoiceField(label="Días permiso" ,choices=DIAS)
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'dias_permiso', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }
        ## ejemplo label
        # labels = {
        #     'dias_permiso': 'Días permiso',
        # }


class PermisoLaboralForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermisoLaboralForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'nombre_del_evento', 'ciudad', 'pais', 'asiste_en_calidad']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'nombre_del_evento': forms.TextInput(attrs={'autocomplete':'off'}),
            'ciudad': forms.TextInput(attrs={'autocomplete':'off'}),
            'pais': forms.TextInput(attrs={'autocomplete':'off'}),
        }


class ComisionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComisionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes', 'nombre_del_evento', 'ciudad', 'pais', 'asiste_en_calidad', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
            'nombre_del_evento': forms.TextInput(attrs={'autocomplete':'off'}),
            'ciudad': forms.TextInput({'autocomplete':'off'}),
            'pais': forms.TextInput(attrs={'autocomplete':'off'}),
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }


class ComisionViaticosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComisionViaticosForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'resolucion_viaticos', 'nombre_del_evento', 'ciudad', 'pais', 'asiste_en_calidad', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'resolucion_viaticos': forms.TextInput(attrs={'type': 'number', 'min': '0', 'autocomplete':'off'}),
            'nombre_del_evento': forms.TextInput(attrs={'autocomplete':'off'}),
            'ciudad': forms.TextInput(attrs={'autocomplete':'off'}),
            'pais': forms.TextInput(attrs={'autocomplete':'off'}),
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }    


class ReservaVacacionesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservaVacacionesForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['resolucion_vaciones', 'no_reserva_rectoria', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'soportes']
        widgets = {
            'no_dias_a_reservar': forms.NumberInput(),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            #'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
        }


class DisfruteVacacionesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisfruteVacacionesForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = [ 'no_dias_a_disfrutar', 'no_reserva_previa', 'fecha_i', 'fecha_f', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'no_dias_a_reservar': forms.NumberInput(),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }


class DisfruteVacaciones2Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisfruteVacaciones2Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_reserva_personal', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'dias_pendientes1', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'autocomplete':'off'}),
            'no_reserva_personal': forms.NumberInput(attrs={'autocomplete':'off'}),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
        }


class ReservaCompensatorio(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservaCompensatorio, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'autocomplete':'off'}),
            'no_dias_a_reservar': forms.NumberInput(attrs={'autocomplete':'off'}),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
        }


class DisfruteCompensatorio(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisfruteCompensatorio, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='soportes':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_dias_a_disfrutar', 'fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'autocomplete':'off'}),
            'no_dias_a_disfrutar': forms.NumberInput(attrs={'autocomplete':'off'}),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
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
    def __init__(self, *args, **kwargs):
        super(ComisionMayorSeisSabaticoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name=='convenio':
                field.widget.attrs['required'] = ''
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'convenio']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
        }


# por si quieren que escriban algo para las modificaciones y correcciones
class JustificacionForm(forms.Form):
    justificacion = forms.CharField(widget=forms.Textarea( attrs={'class': 'form-control', 'cols': 80, 'rows': 2,}))


class ReintegroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReintegroForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Reintegro
        fields = ['cumplido']


## probando código...
class SelectdateForm(forms.Form):
    fecha = forms.DateField(label='Fecha:', 
    widget=forms.SelectDateWidget(years=range(1900,2050), 
    attrs={'class':'form-control',}))


## una forma de hacer formularios
# class EXAMPLE(ModelForm):
#     class Meta:
#         model = Solicitud
#         fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
#         widgets = {
#             'fecha_i': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
#             'fecha_f': forms.DateInput(attrs={'class':'form-control', 'placeholder':'seleccione fecha', 'type': 'date'}),
#             'soportes': forms.FileInput(attrs={'class':'form-control', 'required':''}),
#             'justificacion': forms.Textarea(attrs={'class':'form-control', 'cols': 80, 'rows': 2, 'autocomplete':'off'}),
#             'nombre_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
#             'apellido_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
#             'cargo_encargo': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
#         }

