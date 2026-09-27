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


class FichaMedicaInline(admin.StackedInline):
    model = FichaMedica
    extra = 0
    can_delete = False
    fields = (
        'alergias',
        'antecedentes_familiares',
        'medicamentos_actuales',
        'tipo_seguro',
        'contacto_emergencia',
    )


class VentaInline(admin.TabularInline):
    model = Venta
    extra = 1
    fields = ('producto', 'fecha_venta', 'cantidad', 'precio_unitario', 'estado')


@admin.register(Optometrista)
class OptometristaAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'numero_colegiatura', 'telefono')
    search_fields = ('nombres', 'apellidos', 'numero_colegiatura')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'marca', 'precio', 'stock')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'marca')


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')
    search_fields = ('nombre', 'direccion')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'dni', 'telefono', 'fecha_nacimiento')
    search_fields = ('nombres', 'apellidos', 'dni')
    inlines = [FichaMedicaInline, VentaInline]


@admin.register(HistorialClinico)
class HistorialClinicoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_examen', 'diagnostico')
    list_filter = ('fecha_examen',)
    search_fields = ('diagnostico', 'cliente__nombres', 'cliente__apellidos')


@admin.register(FichaMedica)
class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo_seguro', 'contacto_emergencia')
    search_fields = ('cliente__nombres', 'cliente__apellidos', 'tipo_seguro')


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto', 'fecha_venta', 'cantidad', 'precio_unitario', 'estado')
    list_filter = ('estado', 'fecha_venta')
    search_fields = ('cliente__nombres', 'cliente__apellidos', 'producto__nombre')
