import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Parcela(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    cultivo = models.CharField(max_length=80)
    referencia = models.CharField(max_length=200, blank=True, default='')
    latitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    agricultor = models.CharField(max_length=150)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'parcela'
        verbose_name_plural = 'parcelas'

    def __str__(self):
        return self.nombre

    @property
    def total_diagnosticos(self):
        return self.diagnosticos.count()


class Diagnostico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parcela = models.ForeignKey(
        Parcela,
        on_delete=models.CASCADE,
        related_name='diagnosticos',
    )
    fecha_captura = models.DateTimeField()
    plaga_detectada = models.CharField(max_length=100)
    plaga_nombre = models.CharField(max_length=100)
    confianza = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    imagen_url = models.URLField(blank=True, default='')

    class Meta:
        ordering = ['-fecha_captura']
        verbose_name = 'diagnóstico'
        verbose_name_plural = 'diagnósticos'

    def __str__(self):
        return f'{self.plaga_nombre} — {self.fecha_captura:%Y-%m-%d}'
