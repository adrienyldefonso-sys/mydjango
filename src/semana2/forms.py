from django import forms


class ObjetoEncontradoForm(forms.Form):
    """Formulario para registrar objetos encontrados"""
    
    nombre = forms.CharField(
        max_length=200,
        required=True,
        label="Nombre del objeto",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: Mochila negra',
        })
    )
    
    descripcion = forms.CharField(
        required=True,
        label="Descripción",
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Describe características como color, marca, tamaño o elementos distintivos',
            'rows': 4,
        })
    )
    
    ubicacion = forms.CharField(
        max_length=200,
        required=True,
        label="Ubicación",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: Biblioteca, Aula 305, Cafetería',
        })
    )
    
    fecha = forms.CharField(
        max_length=10,
        required=True,
        label="Fecha encontrado",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'DD/MM/YYYY',
        })
    )
    
    contacto = forms.CharField(
        max_length=200,
        required=True,
        label="Datos de contacto",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nombre y teléfono o correo',
        })
    )
    
    def clean_nombre(self):
        """Valida que el nombre no esté vacío después de limpiar espacios"""
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError("El nombre del objeto es obligatorio")
        return nombre
    
    def clean_descripcion(self):
        """Valida que la descripción tenga al menos 5 caracteres"""
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if len(descripcion) < 5:
            raise forms.ValidationError("La descripción debe tener al menos 5 caracteres")
        return descripcion
    
    def clean_ubicacion(self):
        """Valida que la ubicación no esté vacía"""
        ubicacion = self.cleaned_data.get('ubicacion', '').strip()
        if not ubicacion:
            raise forms.ValidationError("La ubicación es obligatoria")
        return ubicacion
    
    def clean_fecha(self):
        """Valida que la fecha tenga el formato DD/MM/YYYY"""
        fecha = self.cleaned_data.get('fecha', '').strip()
        if not fecha:
            raise forms.ValidationError("La fecha es obligatoria")
        
        # Validar formato DD/MM/YYYY
        partes = fecha.split('/')
        if len(partes) != 3:
            raise forms.ValidationError("La fecha debe estar en formato DD/MM/YYYY")
        
        try:
            dia, mes, año = int(partes[0]), int(partes[1]), int(partes[2])
            if not (1 <= dia <= 31 and 1 <= mes <= 12 and año > 2000):
                raise ValueError
        except (ValueError, IndexError):
            raise forms.ValidationError("Fecha inválida. Use formato DD/MM/YYYY con valores válidos")
        
        return fecha
    
    def clean_contacto(self):
        """Valida que el contacto no esté vacío"""
        contacto = self.cleaned_data.get('contacto', '').strip()
        if not contacto:
            raise forms.ValidationError("Los datos de contacto son obligatorios")
        return contacto
