from django.db import models
from django.db.models import Q


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return self.nombre


class ObjetoEncontradoQuerySet(models.QuerySet):
    def buscar(self, termino):
        termino = (termino or '').strip()
        if not termino:
            return self.all()

        return self.filter(
            Q(nombre__icontains=termino) | Q(ubicacion__nombre__icontains=termino)
        ).order_by('fecha', 'nombre')


class ObjetoEncontradoManager(models.Manager.from_queryset(ObjetoEncontradoQuerySet)):
    def buscar(self, termino):
        return self.get_queryset().buscar(termino)


class ObjetoEncontrado(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name='objetos')
    fecha = models.DateField()
    contacto = models.CharField(max_length=200)

    objects = ObjetoEncontradoManager()

    class Meta:
        ordering = ['-fecha', 'nombre']
        verbose_name = 'Objeto encontrado'
        verbose_name_plural = 'Objetos encontrados'

    def __str__(self):
        return self.nombre
