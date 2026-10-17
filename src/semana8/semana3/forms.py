from django import forms

from .models import Cliente, HistorialClinico, Optometrista, Producto, Sucursal


class OptometristaForm(forms.ModelForm):
    class Meta:
        model = Optometrista
        fields = '__all__'


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = '__all__'


class ClienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HistorialClinicoForm(forms.ModelForm):
    fecha_examen = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = HistorialClinico
        fields = '__all__'
        widgets = {
            'diagnostico': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'esfera_od': forms.NumberInput(attrs={'class': 'form-control'}),
            'cilindro_od': forms.NumberInput(attrs={'class': 'form-control'}),
            'eje_od': forms.NumberInput(attrs={'class': 'form-control'}),
            'esfera_oi': forms.NumberInput(attrs={'class': 'form-control'}),
            'cilindro_oi': forms.NumberInput(attrs={'class': 'form-control'}),
            'eje_oi': forms.NumberInput(attrs={'class': 'form-control'}),
        }
