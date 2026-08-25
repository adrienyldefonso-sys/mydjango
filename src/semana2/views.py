from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import obtener_objetos, obtener_objeto_por_id, agregar_objeto, buscar_objetos
from .forms import ObjetoEncontradoForm


def objeto_list(request):
    """Vista para listar todos los objetos encontrados o buscar"""
    termino_busqueda = request.GET.get('q', '').strip()
    
    if termino_busqueda:
        objetos = buscar_objetos(termino_busqueda)
    else:
        objetos = obtener_objetos()
    
    return render(request, 'semana2/objeto_list.html', {
        'objetos': objetos,
        'termino_busqueda': termino_busqueda,
        'total_resultados': len(objetos)
    })


def objeto_detail(request, objeto_id):
    """Vista para mostrar los detalles de un objeto encontrado"""
    objeto = obtener_objeto_por_id(objeto_id)
    if objeto is None:
        return HttpResponse("Objeto no encontrado", status=404)
    return render(request, 'semana2/objeto_detail.html', {'objeto': objeto})


def objeto_create(request):
    """Vista para crear un nuevo objeto encontrado"""
    if request.method == 'POST':
        form = ObjetoEncontradoForm(request.POST)
        if form.is_valid():
            agregar_objeto(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                ubicacion=form.cleaned_data['ubicacion'],
                fecha=form.cleaned_data['fecha'],
                contacto=form.cleaned_data['contacto']
            )
            return redirect('semana2:objeto_list')
    else:
        form = ObjetoEncontradoForm()
    
    return render(request, 'semana2/objeto_create.html', {'form': form})
