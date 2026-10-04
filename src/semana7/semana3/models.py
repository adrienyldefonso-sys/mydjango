from django.db import models


class Optometrista(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_colegiatura = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Optometrista'
        verbose_name_plural = 'Optometristas'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class Producto(models.Model):
    TIPO_CHOICES = [
        ('armazon', 'Armazón'),
        ('luna', 'Luna'),
        ('lente_contacto', 'Lente de contacto'),
    ]
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=100, blank=True, default='')
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20, blank=True, default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class HistorialClinico(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='historiales'
    )
    fecha_examen = models.DateField()
    diagnostico = models.CharField(max_length=200)
    esfera_od = models.FloatField(null=True, blank=True)
    cilindro_od = models.FloatField(null=True, blank=True)
    eje_od = models.IntegerField(null=True, blank=True)
    esfera_oi = models.FloatField(null=True, blank=True)
    cilindro_oi = models.FloatField(null=True, blank=True)
    eje_oi = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-fecha_examen']
        verbose_name = 'Historial clínico'
        verbose_name_plural = 'Historiales clínicos'

    def __str__(self):
        return f'Historial de {self.cliente} - {self.fecha_examen}'
