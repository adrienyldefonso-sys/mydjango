from django.contrib import admin

from .models import (
    Cliente,
    HistorialClinico,
    Optometrista,
    Producto,
    Sucursal,
)

admin.site.register(Optometrista)
admin.site.register(Producto)
admin.site.register(Sucursal)
admin.site.register(Cliente)
admin.site.register(HistorialClinico)
