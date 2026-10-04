from django.contrib import admin

from .models import (
    Cliente,
    FichaMedica,
    HistorialClinico,
    Optometrista,
    Producto,
    Sucursal,
    Venta,
)

admin.site.register(Optometrista)
admin.site.register(Producto)
admin.site.register(Sucursal)
admin.site.register(Cliente)
admin.site.register(HistorialClinico)
admin.site.register(FichaMedica)
admin.site.register(Venta)
