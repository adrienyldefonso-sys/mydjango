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


@admin.action(description='Cargar datos de prueba de óptica')
def cargar_datos_prueba(modeladmin, request, queryset):
    from datetime import date

    clientes_seed = [
        {'nombres': 'Ana', 'apellidos': 'López', 'dni': '10101010A', 'telefono': '600111111', 'fecha_nacimiento': date(1990, 2, 12)},
        {'nombres': 'Luis', 'apellidos': 'Gómez', 'dni': '20202020B', 'telefono': '600222222', 'fecha_nacimiento': date(1988, 5, 22)},
        {'nombres': 'Marta', 'apellidos': 'Ruiz', 'dni': '30303030C', 'telefono': '600333333', 'fecha_nacimiento': date(1995, 7, 4)},
        {'nombres': 'Pedro', 'apellidos': 'Salas', 'dni': '40404040D', 'telefono': '600444444', 'fecha_nacimiento': date(1979, 11, 16)},
        {'nombres': 'Sofía', 'apellidos': 'Díaz', 'dni': '50505050E', 'telefono': '600555555', 'fecha_nacimiento': date(2001, 1, 8)},
    ]

    productos_seed = [
        {'nombre': 'Armazón Classic', 'tipo': 'armazon', 'marca': 'Ray-Ban', 'precio': '120.00', 'stock': 18},
        {'nombre': 'Luna Blue Light', 'tipo': 'luna', 'marca': 'OptiVision', 'precio': '95.00', 'stock': 25},
        {'nombre': 'Lente Daily Flex', 'tipo': 'lente_contacto', 'marca': 'Acuvue', 'precio': '60.00', 'stock': 40},
        {'nombre': 'Armazón Sport', 'tipo': 'armazon', 'marca': 'Nike Vision', 'precio': '150.00', 'stock': 12},
        {'nombre': 'Luna Pro', 'tipo': 'luna', 'marca': 'Essilor', 'precio': '110.00', 'stock': 20},
    ]

    productos = []
    for data in productos_seed:
        producto, _ = Producto.objects.get_or_create(nombre=data['nombre'], defaults=data)
        productos.append(producto)

    clientes = []
    for data in clientes_seed:
        cliente, _ = Cliente.objects.get_or_create(dni=data['dni'], defaults=data)
        clientes.append(cliente)

    historial_seed = [
        (clientes[0], date(2024, 1, 15), 'Miopía leve', ' -1.00', ' -0.50', 90, ' -2.25', ' -0.75', 110, 'Sin observaciones'),
        (clientes[1], date(2024, 2, 18), 'Astigmatismo moderado', ' -2.50', ' -1.25', 100, ' -1.50', ' -0.25', 95, 'Control cada 6 meses'),
        (clientes[3], date(2024, 3, 12), 'Presbicia', ' -0.50', ' 0.00', 115, ' -1.00', ' 0.50', 120, 'Revisión visual'),
    ]

    for cliente, fecha, diagnostico, esfera_od, cilindro_od, eje_od, esfera_oi, cilindro_oi, eje_oi, observaciones in historial_seed:
        HistorialClinico.objects.get_or_create(
            cliente=cliente,
            fecha_examen=fecha,
            defaults={
                'diagnostico': diagnostico,
                'esfera_od': float(esfera_od),
                'cilindro_od': float(cilindro_od),
                'eje_od': eje_od,
                'esfera_oi': float(esfera_oi),
                'cilindro_oi': float(cilindro_oi),
                'eje_oi': eje_oi,
                'observaciones': observaciones,
            },
        )

    ventas_seed = [
        (clientes[0], productos[0], date(2024, 1, 20), 1, '120.00', 'pendiente'),
        (clientes[0], productos[2], date(2024, 1, 25), 2, '60.00', 'pagado'),
        (clientes[1], productos[1], date(2024, 2, 10), 3, '95.00', 'entregado'),
        (clientes[1], productos[3], date(2024, 2, 15), 1, '150.00', 'pendiente'),
        (clientes[2], productos[0], date(2024, 3, 2), 2, '120.00', 'pagado'),
        (clientes[2], productos[4], date(2024, 3, 6), 1, '110.00', 'entregado'),
        (clientes[3], productos[2], date(2024, 4, 4), 4, '60.00', 'pendiente'),
        (clientes[4], productos[1], date(2024, 4, 12), 2, '95.00', 'pagado'),
    ]

    for cliente, producto, fecha, cantidad, precio, estado in ventas_seed:
        Venta.objects.get_or_create(
            cliente=cliente,
            producto=producto,
            fecha_venta=fecha,
            cantidad=cantidad,
            defaults={'precio_unitario': precio, 'estado': estado},
        )

    modeladmin.message_user(request, 'Datos de prueba cargados: 5 clientes, 3 históricos y 8 ventas.')


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
    actions = [cargar_datos_prueba]


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
