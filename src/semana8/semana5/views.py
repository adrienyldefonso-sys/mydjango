from django.contrib import messages
from django.db import transaction
from django.db.models import Count, F, Sum
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

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
from .serializers import (
    ClienteInvestigacionSerializer,
    ClienteResumenSerializer,
    FichaMedicaReadSerializer,
    ProductoInvestigacionSerializer,
    ProductoSerializer,
    VentaReadSerializer,
)
from semana7.models import ClienteReporte


class ProductoViewSet(ModelViewSet):
    # ModelViewSet reúne las operaciones de lectura y escritura del recurso Producto.
    # El router genera las URLs a partir de este ViewSet y su queryset.
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    # search permite buscar texto en nombre, marca y tipo del producto.
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nombre', 'marca', 'tipo')
    # ordering permite ordenar solo por los campos expresamente permitidos.
    ordering_fields = ('nombre', 'precio', 'stock')
    ordering = ('nombre',)


class ProductoInvestigacionViewSet(ModelViewSet):
    # CRUD del recurso Producto de la investigación propia, con su validación.
    serializer_class = ProductoInvestigacionSerializer
    # Permite búsquedas por nombre, marca o tipo y orden por campos autorizados.
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nombre', 'marca', 'tipo')
    ordering_fields = ('nombre', 'precio', 'stock')
    ordering = ('nombre',)

    def get_queryset(self):
        # Filtro propio de la investigación: ?tipo=luna o ?tipo=armazon.
        queryset = Producto.objects.all()
        tipo = self.request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset


class ClienteInvestigacionViewSet(ModelViewSet):
    # CRUD del recurso Cliente de la investigación propia.
    queryset = Cliente.objects.all()
    serializer_class = ClienteInvestigacionSerializer

    @action(detail=False, methods=('get',), url_path='con-ventas-pendientes')
    def con_ventas_pendientes(self, request):
        # Reutiliza el método del QuerySet personalizado de la Semana 7.
        clientes = ClienteReporte.objects.con_ventas_pendientes()
        serializer = ClienteResumenSerializer(clientes, many=True)
        return Response(serializer.data)


class FichaMedicaReadOnlyViewSet(ReadOnlyModelViewSet):
    # Expone la ficha clínica y el Cliente anidado únicamente en modo lectura.
    serializer_class = FichaMedicaReadSerializer

    def get_queryset(self):
        # FichaMedica.cliente es OneToOneField; select_related evita una
        # consulta adicional por cada ficha al serializar los datos anidados.
        return FichaMedica.objects.select_related('cliente').all()


class VentaReadOnlyViewSet(ReadOnlyModelViewSet):
    # Este ViewSet permite consultar las ventas, pero no crearlas ni modificarlas.
    serializer_class = VentaReadSerializer

    def get_queryset(self):
        # cliente y producto son ForeignKey; select_related los carga en una
        # sola consulta SQL para evitar consultas adicionales por cada venta.
        queryset = Venta.objects.select_related('cliente', 'producto').all()

        # Si se envía ?estado=..., filtramos las ventas por ese estado.
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    @action(detail=False, methods=('get',), url_path='clientes-con-ventas-pendientes')
    def clientes_con_ventas_pendientes(self, request):
        # Reutilizamos el método personalizado definido en semana7.models.
        # Ese QuerySet devuelve clientes que tienen ventas pendientes.
        clientes = ClienteReporte.objects.con_ventas_pendientes()

        # El endpoint de acción entrega los clientes encontrados en formato JSON.
        serializer = ClienteResumenSerializer(clientes, many=True)
        return Response(serializer.data)


# --- Clientes ---
def lista_clientes(request):
    query = request.GET.get('q', '').strip()
    clientes = Cliente.objects.con_ventas_pendientes().select_related('ficha_medica').prefetch_related(
        'historiales', 'ventas__producto'
    ).all()
    if query:
        clientes = clientes.filter(
            dni__icontains=query
        ) | clientes.filter(apellidos__icontains=query)
        clientes = clientes.distinct().order_by('apellidos', 'nombres')
    else:
        clientes = clientes.order_by('apellidos', 'nombres')
    return render(request, 'semana5/cliente_list.html', {'clientes': clientes, 'query': query})


def lista_clientes_relacionados(request):
    clientes = Cliente.objects.del_mes_actual().select_related('ficha_medica').prefetch_related(
        'historiales', 'ventas__producto'
    ).all()
    return render(request, 'semana5/cliente_list.html', {'clientes': clientes, 'query': '', 'solo_relaciones': True})


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_clientes')
    else:
        form = ClienteForm()
    return render(request, 'semana5/cliente_form.html', {'form': form, 'titulo': 'Crear cliente', 'cancel_url': '/optica-v3/clientes/'})


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'semana5/cliente_form.html', {'form': form, 'titulo': 'Editar cliente', 'cancel_url': '/optica-v3/clientes/'})


def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('semana5:listado_clientes')
    return render(request, 'semana5/cliente_confirm_delete.html', {'objeto': cliente, 'titulo': 'Eliminar cliente'})


# --- Historiales ---
def lista_historiales(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    historiales = HistorialClinico.objects.select_related('cliente').filter(cliente=cliente).order_by('-fecha_examen')
    return render(request, 'semana5/historialclinico_list.html', {'cliente': cliente, 'historiales': historiales})


def crear_historial(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.cliente = cliente
            historial.save()
            return redirect('semana5:listado_historiales', cliente_id=cliente.id)
    else:
        form = HistorialClinicoForm(initial={'cliente': cliente})
    return render(request, 'semana5/historialclinico_form.html', {'form': form, 'cliente': cliente, 'titulo': 'Crear historial', 'cancel_url': f'/optica-v3/historiales/{cliente.id}/'})


def editar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_historiales', cliente_id=historial.cliente_id)
    else:
        form = HistorialClinicoForm(instance=historial)
    return render(request, 'semana5/historialclinico_form.html', {'form': form, 'cliente': historial.cliente, 'titulo': 'Editar historial', 'cancel_url': f'/optica-v3/historiales/{historial.cliente_id}/'})


def eliminar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, pk=pk)
    if request.method == 'POST':
        cliente_id = historial.cliente_id
        historial.delete()
        return redirect('semana5:listado_historiales', cliente_id=cliente_id)
    return render(request, 'semana5/historialclinico_confirm_delete.html', {'objeto': historial, 'titulo': 'Eliminar historial'})


# --- Optometristas ---
def lista_optometristas(request):
    optometristas = Optometrista.objects.all()
    return render(request, 'semana5/optometrista_list.html', {'optometristas': optometristas})


def crear_optometrista(request):
    if request.method == 'POST':
        form = OptometristaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_optometristas')
    else:
        form = OptometristaForm()
    return render(request, 'semana5/optometrista_form.html', {'form': form, 'titulo': 'Crear optometrista', 'cancel_url': '/optica-v3/optometristas/'})


def editar_optometrista(request, pk):
    optometrista = get_object_or_404(Optometrista, pk=pk)
    if request.method == 'POST':
        form = OptometristaForm(request.POST, instance=optometrista)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_optometristas')
    else:
        form = OptometristaForm(instance=optometrista)
    return render(request, 'semana5/optometrista_form.html', {'form': form, 'titulo': 'Editar optometrista', 'cancel_url': '/optica-v3/optometristas/'})


def eliminar_optometrista(request, pk):
    optometrista = get_object_or_404(Optometrista, pk=pk)
    if request.method == 'POST':
        optometrista.delete()
        return redirect('semana5:listado_optometristas')
    return render(request, 'semana5/optometrista_confirm_delete.html', {'objeto': optometrista, 'titulo': 'Eliminar optometrista'})


# --- Productos ---
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'semana5/producto_list.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_productos')
    else:
        form = ProductoForm()
    return render(request, 'semana5/producto_form.html', {'form': form, 'titulo': 'Crear producto', 'cancel_url': '/optica-v3/productos/'})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'semana5/producto_form.html', {'form': form, 'titulo': 'Editar producto', 'cancel_url': '/optica-v3/productos/'})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('semana5:listado_productos')
    return render(request, 'semana5/producto_confirm_delete.html', {'objeto': producto, 'titulo': 'Eliminar producto'})


# --- Sucursales ---
def lista_sucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'semana5/sucursal_list.html', {'sucursales': sucursales})


def crear_sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_sucursales')
    else:
        form = SucursalForm()
    return render(request, 'semana5/sucursal_form.html', {'form': form, 'titulo': 'Crear sucursal', 'cancel_url': '/optica-v3/sucursales/'})


def editar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_sucursales')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'semana5/sucursal_form.html', {'form': form, 'titulo': 'Editar sucursal', 'cancel_url': '/optica-v3/sucursales/'})


def eliminar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('semana5:listado_sucursales')
    return render(request, 'semana5/sucursal_confirm_delete.html', {'objeto': sucursal, 'titulo': 'Eliminar sucursal'})


# --- Fichas médicas ---
def lista_fichas_medicas(request):
    fichas = FichaMedica.objects.select_related('cliente').all()
    return render(request, 'semana5/fichamedica_list.html', {'fichas': fichas})


def crear_ficha_medica(request):
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_fichas_medicas')
    else:
        form = FichaMedicaForm()
    return render(request, 'semana5/fichamedica_form.html', {'form': form, 'titulo': 'Crear ficha médica', 'cancel_url': '/optica-v3/fichas-medicas/'})


def editar_ficha_medica(request, pk):
    ficha = get_object_or_404(FichaMedica, pk=pk)
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_fichas_medicas')
    else:
        form = FichaMedicaForm(instance=ficha)
    return render(request, 'semana5/fichamedica_form.html', {'form': form, 'titulo': 'Editar ficha médica', 'cancel_url': '/optica-v3/fichas-medicas/'})


def eliminar_ficha_medica(request, pk):
    ficha = get_object_or_404(FichaMedica, pk=pk)
    if request.method == 'POST':
        ficha.delete()
        return redirect('semana5:listado_fichas_medicas')
    return render(request, 'semana5/fichamedica_confirm_delete.html', {'objeto': ficha, 'titulo': 'Eliminar ficha médica'})


# --- Ventas ---
def lista_ventas(request):
    ventas = Venta.objects.select_related('cliente', 'producto').all()
    return render(request, 'semana5/venta_list.html', {'ventas': ventas})


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_ventas')
    else:
        form = VentaForm()
    return render(request, 'semana5/venta_form.html', {'form': form, 'titulo': 'Crear venta', 'cancel_url': '/optica-v3/ventas/'})


def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('semana5:listado_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'semana5/venta_form.html', {'form': form, 'titulo': 'Editar venta', 'cancel_url': '/optica-v3/ventas/'})


def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('semana5:listado_ventas')
    return render(request, 'semana5/venta_confirm_delete.html', {'objeto': venta, 'titulo': 'Eliminar venta'})


def registrar_venta(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                producto = Producto.objects.select_for_update().get(pk=request.POST['producto_id'])
                cantidad = int(request.POST['cantidad'])

                if producto.stock < cantidad:
                    raise ValueError('Stock insuficiente')

                producto.stock = F('stock') - cantidad
                producto.save(update_fields=['stock'])

                Venta.objects.create(
                    cliente_id=request.POST['cliente_id'],
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    estado='pendiente',
                    fecha_venta=__import__('datetime').date.today(),
                )
            messages.success(request, 'Venta registrada correctamente.')
            return redirect('semana5:registrar_venta')
        except Exception as exc:
            messages.error(request, f'No se pudo registrar la venta: {exc}')
            return redirect('semana5:registrar_venta')

    productos = Producto.objects.all().order_by('nombre')
    clientes = Cliente.objects.all().order_by('apellidos', 'nombres')
    return render(request, 'semana5/registrar_venta.html', {'productos': productos, 'clientes': clientes})


def reporte_view(request):
    total = Venta.objects.aggregate(total_general=Sum(F('cantidad') * F('precio_unitario')))
    clientes_con_ventas = Cliente.objects.annotate(num_ventas=Count('ventas')).order_by('-num_ventas')
    ventas_por_estado = Venta.objects.values('estado').annotate(total=Count('id')).order_by('-total')
    return render(request, 'semana5/reporte.html', {
        'total': total['total_general'],
        'clientes_con_ventas': clientes_con_ventas,
        'ventas_por_estado': ventas_por_estado,
    })
