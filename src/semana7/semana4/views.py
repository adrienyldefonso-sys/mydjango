from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ClienteForm,
    FichaMedicaForm,
    HistorialClinicoForm,
    OptometristaForm,
    ProductoForm,
    SucursalForm,
    VentaForm,
)
from .models import (
    Cliente,
    FichaMedica,
    HistorialClinico,
    Optometrista,
    Producto,
    Sucursal,
    Venta,
)


# --- Clientes ---
def lista_clientes(request):
    query = request.GET.get('q', '').strip()
    clientes = Cliente.objects.select_related('ficha_medica').prefetch_related(
        'historiales', 'ventas__producto'
    ).all()
    if query:
        clientes = clientes.filter(
            dni__icontains=query
        ) | clientes.filter(apellidos__icontains=query)
        clientes = clientes.distinct().order_by('apellidos', 'nombres')
    else:
        clientes = clientes.order_by('apellidos', 'nombres')
    return render(request, 'semana4/cliente_list.html', {'clientes': clientes, 'query': query})


def lista_clientes_relacionados(request):
    clientes = Cliente.objects.select_related('ficha_medica').prefetch_related(
        'historiales', 'ventas__producto'
    ).all()
    return render(request, 'semana4/cliente_list.html', {'clientes': clientes, 'query': '', 'solo_relaciones': True})


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_clientes')
    else:
        form = ClienteForm()
    return render(request, 'semana4/cliente_form.html', {'form': form, 'titulo': 'Crear cliente', 'cancel_url': '/optica-v2/clientes/'})


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'semana4/cliente_form.html', {'form': form, 'titulo': 'Editar cliente', 'cancel_url': '/optica-v2/clientes/'})


def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('semana4:listado_clientes')
    return render(request, 'semana4/cliente_confirm_delete.html', {'objeto': cliente, 'titulo': 'Eliminar cliente'})


# --- Historiales ---
def lista_historiales(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    historiales = HistorialClinico.objects.select_related('cliente').filter(cliente=cliente).order_by('-fecha_examen')
    return render(request, 'semana4/historialclinico_list.html', {'cliente': cliente, 'historiales': historiales})


def crear_historial(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.cliente = cliente
            historial.save()
            return redirect('semana4:listado_historiales', cliente_id=cliente.id)
    else:
        form = HistorialClinicoForm(initial={'cliente': cliente})
    return render(request, 'semana4/historialclinico_form.html', {'form': form, 'cliente': cliente, 'titulo': 'Crear historial', 'cancel_url': f'/optica-v2/historiales/{cliente.id}/'})


def editar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_historiales', cliente_id=historial.cliente_id)
    else:
        form = HistorialClinicoForm(instance=historial)
    return render(request, 'semana4/historialclinico_form.html', {'form': form, 'cliente': historial.cliente, 'titulo': 'Editar historial', 'cancel_url': f'/optica-v2/historiales/{historial.cliente_id}/'})


def eliminar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        cliente_id = historial.cliente_id
        historial.delete()
        return redirect('semana4:listado_historiales', cliente_id=cliente_id)
    return render(request, 'semana4/historialclinico_confirm_delete.html', {'objeto': historial, 'titulo': 'Eliminar historial'})


# --- Optometristas ---
def lista_optometristas(request):
    optometristas = Optometrista.objects.all()
    return render(request, 'semana4/optometrista_list.html', {'optometristas': optometristas})


def crear_optometrista(request):
    if request.method == 'POST':
        form = OptometristaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_optometristas')
    else:
        form = OptometristaForm()
    return render(request, 'semana4/optometrista_form.html', {'form': form, 'titulo': 'Crear optometrista', 'cancel_url': '/optica-v2/optometristas/'})


def editar_optometrista(request, pk):
    optometrista = get_object_or_404(Optometrista, pk=pk)
    if request.method == 'POST':
        form = OptometristaForm(request.POST, instance=optometrista)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_optometristas')
    else:
        form = OptometristaForm(instance=optometrista)
    return render(request, 'semana4/optometrista_form.html', {'form': form, 'titulo': 'Editar optometrista', 'cancel_url': '/optica-v2/optometristas/'})


def eliminar_optometrista(request, pk):
    optometrista = get_object_or_404(Optometrista, pk=pk)
    if request.method == 'POST':
        optometrista.delete()
        return redirect('semana4:listado_optometristas')
    return render(request, 'semana4/optometrista_confirm_delete.html', {'objeto': optometrista, 'titulo': 'Eliminar optometrista'})


# --- Productos ---
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'semana4/producto_list.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_productos')
    else:
        form = ProductoForm()
    return render(request, 'semana4/producto_form.html', {'form': form, 'titulo': 'Crear producto', 'cancel_url': '/optica-v2/productos/'})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'semana4/producto_form.html', {'form': form, 'titulo': 'Editar producto', 'cancel_url': '/optica-v2/productos/'})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('semana4:listado_productos')
    return render(request, 'semana4/producto_confirm_delete.html', {'objeto': producto, 'titulo': 'Eliminar producto'})


# --- Sucursales ---
def lista_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'semana4/sucursal_list.html', {'sucursales': sucursales})


def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_sucursales')
    else:
        form = SucursalForm()
    return render(request, 'semana4/sucursal_form.html', {'form': form, 'titulo': 'Crear sucursal', 'cancel_url': '/optica-v2/sucursales/'})


def editar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_sucursales')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'semana4/sucursal_form.html', {'form': form, 'titulo': 'Editar sucursal', 'cancel_url': '/optica-v2/sucursales/'})


def eliminar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('semana4:listado_sucursales')
    return render(request, 'semana4/sucursal_confirm_delete.html', {'objeto': sucursal, 'titulo': 'Eliminar sucursal'})


# --- Fichas médicas ---
def lista_fichas_medicas(request):
    fichas = FichaMedica.objects.select_related('cliente').all()
    return render(request, 'semana4/fichamedica_list.html', {'fichas': fichas})


def crear_ficha_medica(request):
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_fichas_medicas')
    else:
        form = FichaMedicaForm()
    return render(request, 'semana4/fichamedica_form.html', {'form': form, 'titulo': 'Crear ficha médica', 'cancel_url': '/optica-v2/fichas-medicas/'})


def editar_ficha_medica(request, pk):
    ficha = get_object_or_404(FichaMedica, pk=pk)
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_fichas_medicas')
    else:
        form = FichaMedicaForm(instance=ficha)
    return render(request, 'semana4/fichamedica_form.html', {'form': form, 'titulo': 'Editar ficha médica', 'cancel_url': '/optica-v2/fichas-medicas/'})


def eliminar_ficha_medica(request, pk):
    ficha = get_object_or_404(FichaMedica, pk=pk)
    if request.method == 'POST':
        ficha.delete()
        return redirect('semana4:listado_fichas_medicas')
    return render(request, 'semana4/fichamedica_confirm_delete.html', {'objeto': ficha, 'titulo': 'Eliminar ficha médica'})


# --- Ventas ---
def lista_ventas(request):
    ventas = Venta.objects.select_related('cliente', 'producto').all()
    return render(request, 'semana4/venta_list.html', {'ventas': ventas})


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_ventas')
    else:
        form = VentaForm()
    return render(request, 'semana4/venta_form.html', {'form': form, 'titulo': 'Crear venta', 'cancel_url': '/optica-v2/ventas/'})


def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('semana4:listado_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'semana4/venta_form.html', {'form': form, 'titulo': 'Editar venta', 'cancel_url': '/optica-v2/ventas/'})


def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('semana4:listado_ventas')
    return render(request, 'semana4/venta_confirm_delete.html', {'objeto': venta, 'titulo': 'Eliminar venta'})
