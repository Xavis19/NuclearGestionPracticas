"""
Formularios para las vistas basadas en templates
"""
from django import forms
from apps.usuarios.models import User
from apps.vacantes.models import Vacante, Empresa


class LoginForm(forms.Form):
    """Formulario de login"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )


class EstudianteForm(forms.ModelForm):
    """Formulario para crear/editar estudiantes"""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'matricula', 'carrera', 'semestre']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
        }
    
    def __init__(self, *args, **kwargs):
        self.edit = kwargs.pop('edit', False)
        super().__init__(*args, **kwargs)
        
        if not self.edit:
            self.fields['password1'].required = True
            self.fields['password2'].required = True
        else:
            # Si estamos editando, las contraseñas no son obligatorias
            del self.fields['password1']
            del self.fields['password2']
    
    def clean(self):
        cleaned_data = super().clean()
        if not self.edit:
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')
            
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')
        
        return cleaned_data


class VacanteForm(forms.ModelForm):
    """Formulario para crear/editar vacantes"""
    
    class Meta:
        model = Vacante
        fields = [
            'empresa', 'titulo', 'descripcion', 'requisitos', 'carreras_solicitadas',
            'semestre_minimo', 'promedio_minimo', 'area', 'modalidad', 'ubicacion',
            'horario', 'duracion_meses', 'vacantes_disponibles', 'fecha_inicio',
            'fecha_cierre_convocatoria', 'remunerada', 'monto_apoyo', 'beneficios_adicionales'
        ]
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'carreras_solicitadas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingeniería, Administración, etc.'}),
            'semestre_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'promedio_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'horario': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion_meses': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'vacantes_disponibles': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_cierre_convocatoria': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remunerada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'monto_apoyo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'beneficios_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
