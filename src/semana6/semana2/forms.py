from django import forms

from .models import ObjetoEncontrado, Ubicacion


class UbicacionForm(forms.ModelForm):
    """Formulario para crear nuevas ubicaciones."""

    class Meta:
        model = Ubicacion
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Biblioteca, Patio principal, Aula 305',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe esta ubicación o su uso dentro de la institución',
                'rows': 3,
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre de la ubicación es obligatorio')
        return nombre


class ObjetoEncontradoForm(forms.ModelForm):
    """Formulario para registrar objetos encontrados."""

    fecha = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label='Fecha encontrado',
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'form-input',
                'placeholder': 'DD/MM/YYYY',
            }
        )
    )
    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.all().order_by('nombre'),
        label='Ubicación',
        empty_label='Seleccione una ubicación',
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = ObjetoEncontrado
        fields = ['nombre', 'descripcion', 'ubicacion', 'fecha', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Mochila negra',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe características como color, marca, tamaño o elementos distintivos',
                'rows': 4,
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nombre y teléfono o correo',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre del objeto es obligatorio')
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if len(descripcion) < 5:
            raise forms.ValidationError('La descripción debe tener al menos 5 caracteres')
        return descripcion

    def clean_contacto(self):
        contacto = self.cleaned_data.get('contacto', '').strip()
        if not contacto:
            raise forms.ValidationError('Los datos de contacto son obligatorios')
        return contacto
