from decimal import Decimal

from rest_framework import serializers

# Importamos DRF para crear serializadores y validar datos JSON.
# Importamos el modelo real que se va a exponer como API.
# El recurso elegido es Producto porque tiene la regla de negocio de precio > 0.
from .models import Cliente, FichaMedica, Producto, Venta


class ProductoSerializer(serializers.ModelSerializer):
    # Heredamos de ModelSerializer para automatizar la conversión entre
    # el modelo Django y el formato JSON que devuelve la API REST.
    # Es la base del recurso simple que se expone en los ejercicios.

    def validate_precio(self, value):
        # Esta validación es propia del negocio: un precio de 0 o menos
        # no tiene sentido para este catálogo de optica.
        if value is None or Decimal(str(value)) <= Decimal('0.00'):
            raise serializers.ValidationError('El precio debe ser mayor que cero.')
        return value

    class Meta:
        # Indicamos sobre qué modelo se trabaja: Producto.
        model = Producto

        # Con '__all__' exportamos todos los campos del modelo para que el
        # JSON completo del recurso quede listo para la API.
        fields = '__all__'


class ClienteResumenSerializer(serializers.ModelSerializer):
    # Representa los datos básicos del cliente dentro de una venta anidada.
    class Meta:
        model = Cliente
        fields = ('id', 'nombres', 'apellidos', 'dni')


class ProductoResumenSerializer(serializers.ModelSerializer):
    # Representa los datos básicos del producto dentro de una venta anidada.
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'tipo', 'marca', 'precio')


class VentaReadSerializer(serializers.ModelSerializer):
    # Estas relaciones se muestran como objetos anidados, no solo como IDs.
    cliente = ClienteResumenSerializer(read_only=True)
    producto = ProductoResumenSerializer(read_only=True)

    class Meta:
        # La venta es el recurso relacionado que se expondrá en modo lectura.
        model = Venta
        fields = (
            'id',
            'cliente',
            'producto',
            'fecha_venta',
            'cantidad',
            'precio_unitario',
            'estado',
        )


class ProductoInvestigacionSerializer(serializers.ModelSerializer):
    # Serializer del recurso simple de la investigación propia.
    # La regla de negocio impide registrar productos con precio cero o negativo.
    def validate_precio(self, value):
        if value is None or Decimal(str(value)) <= Decimal('0.00'):
            raise serializers.ValidationError('El precio debe ser mayor que cero.')
        return value

    class Meta:
        model = Producto
        fields = '__all__'


class ClienteInvestigacionSerializer(serializers.ModelSerializer):
    # Serializer de Cliente, una de las entidades principales de la investigación.
    class Meta:
        model = Cliente
        fields = '__all__'


class FichaMedicaInvestigacionSerializer(serializers.ModelSerializer):
    # Serializer de la entidad asociada uno a uno con Cliente.
    class Meta:
        model = FichaMedica
        fields = '__all__'


class FichaMedicaReadSerializer(serializers.ModelSerializer):
    # Incluye los datos básicos del Cliente asociado uno a uno a la ficha.
    cliente = ClienteResumenSerializer(read_only=True)

    class Meta:
        model = FichaMedica
        fields = (
            'id',
            'cliente',
            'alergias',
            'antecedentes_familiares',
            'medicamentos_actuales',
            'tipo_seguro',
            'contacto_emergencia',
        )


class VentaInvestigacionSerializer(serializers.ModelSerializer):
    # Serializa la relación Cliente-Producto junto con cantidad, fecha y estado.
    # Las entidades relacionadas se representan anidadas y quedan en solo lectura.
    cliente = ClienteResumenSerializer(read_only=True)
    producto = ProductoResumenSerializer(read_only=True)

    class Meta:
        model = Venta
        fields = (
            'id',
            'cliente',
            'producto',
            'fecha_venta',
            'cantidad',
            'precio_unitario',
            'estado',
        )
