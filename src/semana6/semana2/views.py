from django.shortcuts import get_object_or_404, redirect, render

from .forms import ObjetoEncontradoForm, UbicacionForm
from .models import ObjetoEncontrado


def objeto_list(request):
    """Vista para listar todos los objetos encontrados o buscar."""
    termino_busqueda = request.GET.get('q', '').strip()

    if termino_busqueda:
        objetos = ObjetoEncontrado.objects.buscar(termino_busqueda)
    else:
        objetos = ObjetoEncontrado.objects.all()

    return render(request, 'semana2/objeto_list.html', {
        'objetos': objetos,
        'termino_busqueda': termino_busqueda,
        'total_resultados': objetos.count(),
    })


def objeto_detail(request, objeto_id):
    """Vista para mostrar los detalles de un objeto encontrado."""
    objeto = get_object_or_404(ObjetoEncontrado, pk=objeto_id)
    return render(request, 'semana2/objeto_detail.html', {'objeto': objeto})


def ubicacion_create(request):
    """Vista para crear una nueva ubicación y dejarla disponible para escoger."""
    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana2:objeto_create')
    else:
        form = UbicacionForm()

    return render(request, 'semana2/ubicacion_create.html', {'form': form})


def objeto_create(request):
    """Vista para crear un nuevo objeto encontrado."""
    if request.method == 'POST':
        form = ObjetoEncontradoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semana2:objeto_list')
    else:
        form = ObjetoEncontradoForm()

    return render(request, 'semana2/objeto_create.html', {'form': form})
