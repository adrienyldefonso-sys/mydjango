from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ClienteForm,
    HistorialClinicoForm,
    OptometristaForm,
    ProductoForm,
    SucursalForm,
)
from .models import Cliente, HistorialClinico, Optometrista, Producto, Sucursal


def lista_clientes(request):
    query = request.GET.get('q', '').strip()
    if query:
        clientes = Cliente.objects.filter(
            dni__icontains=query
        ) | Cliente.objects.filter(apellidos__icontains=query)
        clientes = clientes.distinct().order_by('apellidos', 'nombres')
    else:
        clientes = Cliente.objects.all()
    return render(request, 'semana3/cliente_list.html', {'clientes': clientes, 'query': query})


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_clientes')
    else:
        form = ClienteForm()
    return render(request, 'semana3/cliente_form.html', {'form': form, 'titulo': 'Crear cliente'})


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'semana3/cliente_form.html', {'form': form, 'titulo': 'Editar cliente'})


def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('semana3:listado_clientes')
    return render(request, 'semana3/cliente_confirm_delete.html', {'objeto': cliente, 'titulo': 'Eliminar cliente'})


def lista_historiales(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    historiales = cliente.historiales.all().order_by('-fecha_examen')
    return render(request, 'semana3/historialclinico_list.html', {'cliente': cliente, 'historiales': historiales})


def crear_historial(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.cliente = cliente
            historial.save()
            return redirect('semana3:listado_historiales', cliente_id=cliente.id)
    else:
        form = HistorialClinicoForm(initial={'cliente': cliente})
    return render(request, 'semana3/historialclinico_form.html', {'form': form, 'cliente': cliente, 'titulo': 'Crear historial'})


def editar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_historiales', cliente_id=historial.cliente_id)
    else:
        form = HistorialClinicoForm(instance=historial)
    return render(request, 'semana3/historialclinico_form.html', {'form': form, 'cliente': historial.cliente, 'titulo': 'Editar historial'})


def eliminar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        cliente_id = historial.cliente_id
        historial.delete()
        return redirect('semana3:listado_historiales', cliente_id=cliente_id)
    return render(request, 'semana3/historialclinico_confirm_delete.html', {'objeto': historial, 'titulo': 'Eliminar historial'})


def lista_optometristas(request):
    optometristas = Optometrista.objects.all()
    return render(request, 'semana3/optometrista_list.html', {'optometristas': optometristas})


def crear_optometrista(request):
    if request.method == 'POST':
        form = OptometristaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_optometristas')
    else:
        form = OptometristaForm()
    return render(request, 'semana3/optometrista_form.html', {'form': form, 'titulo': 'Crear optometrista'})


def editar_optometrista(request, pk):
    optometrista = get_object_or_404(Optometrista, pk=pk)
    if request.method == 'POST':
        form = OptometristaForm(request.POST, instance=optometrista)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_optometristas')
    else:
        form = OptometristaForm(instance=optometrista)
    return render(request, 'semana3/optometrista_form.html', {'form': form, 'titulo': 'Editar optometrista'})


def eliminar_optometrista(request, pk):
    optometrista = get_object_or_404(Optometrista, pk=pk)
    if request.method == 'POST':
        optometrista.delete()
        return redirect('semana3:listado_optometristas')
    return render(request, 'semana3/optometrista_confirm_delete.html', {'objeto': optometrista, 'titulo': 'Eliminar optometrista'})


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'semana3/producto_list.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_productos')
    else:
        form = ProductoForm()
    return render(request, 'semana3/producto_form.html', {'form': form, 'titulo': 'Crear producto'})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'semana3/producto_form.html', {'form': form, 'titulo': 'Editar producto'})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('semana3:listado_productos')
    return render(request, 'semana3/producto_confirm_delete.html', {'objeto': producto, 'titulo': 'Eliminar producto'})


def lista_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'semana3/sucursal_list.html', {'sucursales': sucursales})


def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_sucursales')
    else:
        form = SucursalForm()
    return render(request, 'semana3/sucursal_form.html', {'form': form, 'titulo': 'Crear sucursal'})


def editar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('semana3:listado_sucursales')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'semana3/sucursal_form.html', {'form': form, 'titulo': 'Editar sucursal'})


def eliminar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('semana3:listado_sucursales')
    return render(request, 'semana3/sucursal_confirm_delete.html', {'objeto': sucursal, 'titulo': 'Eliminar sucursal'})
