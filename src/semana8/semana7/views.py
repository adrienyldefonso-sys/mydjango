from datetime import date

from django.contrib import messages
from django.db import transaction
from django.db.models import Count, F, Prefetch, Q, Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from semana5.models import Cliente, Producto, Venta
from .models import ClienteReporte


def registrar_venta(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                producto = Producto.objects.select_for_update().get(pk=request.POST['producto_id'])
                cantidad = int(request.POST['cantidad'])

                if producto.stock < cantidad:
                    raise ValueError('Stock insuficiente')

                Producto.objects.filter(pk=producto.pk).update(stock=F('stock') - cantidad)

                Venta.objects.create(
                    cliente_id=request.POST['cliente_id'],
                    producto_id=producto.pk,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    estado='pendiente',
                    fecha_venta=date.today(),
                )

            messages.success(request, 'Venta registrada correctamente.')
            return redirect('semana7:registrar_venta')
        except Exception as exc:
            messages.error(request, f'No se pudo registrar la venta: {exc}')
            return redirect('semana7:registrar_venta')

    productos = Producto.objects.all().order_by('nombre')
    clientes = Cliente.objects.all().order_by('apellidos', 'nombres')
    clientes_pendientes = ClienteReporte.objects.con_ventas_pendientes()
    return render(request, 'semana7/registrar_venta.html', {
        'productos': productos,
        'clientes': clientes,
        'clientes_pendientes': clientes_pendientes,
    })


def reporte(request):
    total = Venta.objects.aggregate(total_general=Sum(F('cantidad') * F('precio_unitario')))
    clientes_con_ventas = Cliente.objects.annotate(num_ventas=Count('ventas')).order_by('-num_ventas')
    ventas_por_estado = Venta.objects.values('estado').annotate(total=Count('id')).order_by('-total')

    hoy = timezone.localdate()
    ventas_relevantes = Venta.objects.filter(
        Q(estado='pendiente') |
        Q(fecha_venta__year=hoy.year, fecha_venta__month=hoy.month)
    )
    clientes_con_ventas = list(clientes_con_ventas.prefetch_related(
        Prefetch('ventas', queryset=ventas_relevantes)
    ))
    clientes_pendientes = []
    clientes_mes = []
    for cliente in clientes_con_ventas:
        ventas = cliente.ventas.all()
        if any(venta.estado == 'pendiente' for venta in ventas):
            clientes_pendientes.append(cliente)
        if any(
            venta.fecha_venta.year == hoy.year and venta.fecha_venta.month == hoy.month
            for venta in ventas
        ):
            clientes_mes.append(cliente)

    clientes_pendientes.sort(key=lambda cliente: (cliente.apellidos, cliente.nombres))
    clientes_mes.sort(key=lambda cliente: (cliente.apellidos, cliente.nombres))

    return render(request, 'semana7/reporte.html', {
        'total': total['total_general'] or 0,
        'clientes_con_ventas': clientes_con_ventas,
        'ventas_por_estado': ventas_por_estado,
        'clientes_pendientes': clientes_pendientes,
        'clientes_mes': clientes_mes,
    })
