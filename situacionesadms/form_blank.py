from django.forms import ModelForm
from .models import Solicitud
from django import forms


# para colocar type date alos inputs
class DateInput2(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class BasicFormBlank(ModelForm):
    # def __init__(self, *args, **kwargs): 
    #     super(BasicForm, self).__init__(*args, **kwargs)                       
    #     self.fields['__all__'].disabled = True
    def __init__(self, *args, **kwargs):
        super(BasicFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2()
        }


class ConJustificacionFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConJustificacionFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            # format="%d-%m-%Y",
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
        }
    

class ConEncargoFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConEncargoFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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


class JustificacionYEncargoFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(JustificacionYEncargoFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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


class PermisoRemuneradoFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermisoRemuneradoFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    DIAS = [(1,"1"),(2,"2"),(3,"3")]
    dias_permiso = forms.ChoiceField(label="Días permiso" ,choices=DIAS)
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'dias_permiso', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'fecha_i': DateInput2,
            'fecha_f': DateInput2,
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }
        ## ejemplo label
        # labels = {
        #     'dias_permiso': 'Días permiso',
        # }


class PermisoLaboralFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermisoLaboralFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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


class ComisionFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComisionFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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


class ComisionViaticosFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComisionViaticosFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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


class ReservaVacacionesFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservaVacacionesFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Solicitud
        fields = ['resolucion_vaciones', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'justificacion', 'soportes']
        widgets = {
            'resolucion_vaciones': forms.TextInput(),
            'no_dias_a_reservar': forms.NumberInput(),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'justificacion': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'autocomplete':'off'}),
        }


class DisfruteVacacionesFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisfruteVacacionesFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_reserva_personal', 'no_dias_a_disfrutar', 'fecha_i', 'fecha_f', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(),
            'no_reserva_personal': forms.NumberInput(),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
            'nombre_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'apellido_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
            'cargo_encargo': forms.TextInput(attrs={'autocomplete':'off'}),
        }


class DisfruteVacaciones2FormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisfruteVacaciones2FormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Solicitud
        fields = ['no_reserva_rectoria', 'no_reserva_personal', 'no_dias_a_reservar', 'fecha_i', 'fecha_f', 'dias_pendientes1', 'nombre_encargo', 'apellido_encargo', 'cargo_encargo']
        widgets = {
            'no_reserva_rectoria': forms.TextInput(attrs={'autocomplete':'off'}),
            'no_reserva_personal': forms.NumberInput(attrs={'autocomplete':'off'}),
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
        }


class ReservaCompensatorioBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservaCompensatorioBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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


class DisfruteCompensatorioBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisfruteCompensatorioBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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

class ComisionMayorSeisSabaticoFormBlank(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComisionMayorSeisSabaticoFormBlank, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Solicitud
        fields = ['fecha_i', 'fecha_f', 'soportes', 'convenio']
        widgets = {
            'fecha_i': DateInput2(),
            'fecha_f': DateInput2(),
        }
