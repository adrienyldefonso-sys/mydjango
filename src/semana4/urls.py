from django.urls import path

from . import views

app_name = 'semana4'

urlpatterns = [
    path('clientes/', views.lista_clientes, name='listado_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/relacionados/', views.lista_clientes_relacionados, name='listado_clientes_relacionados'),

    path('historiales/<int:cliente_id>/', views.lista_historiales, name='listado_historiales'),
    path('historiales/<int:cliente_id>/nuevo/', views.crear_historial, name='crear_historial'),
    path('historiales/<int:pk>/editar/', views.editar_historial, name='editar_historial'),
    path('historiales/<int:pk>/eliminar/', views.eliminar_historial, name='eliminar_historial'),

    path('optometristas/', views.lista_optometristas, name='listado_optometristas'),
    path('optometristas/nuevo/', views.crear_optometrista, name='crear_optometrista'),
    path('optometristas/<int:pk>/editar/', views.editar_optometrista, name='editar_optometrista'),
    path('optometristas/<int:pk>/eliminar/', views.eliminar_optometrista, name='eliminar_optometrista'),

    path('productos/', views.lista_productos, name='listado_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    path('sucursales/', views.lista_sucursales, name='listado_sucursales'),
    path('sucursales/nuevo/', views.crear_sucursal, name='crear_sucursal'),
    path('sucursales/<int:pk>/editar/', views.editar_sucursal, name='editar_sucursal'),
    path('sucursales/<int:pk>/eliminar/', views.eliminar_sucursal, name='eliminar_sucursal'),

    path('fichas-medicas/', views.lista_fichas_medicas, name='listado_fichas_medicas'),
    path('fichas-medicas/nueva/', views.crear_ficha_medica, name='crear_ficha_medica'),
    path('fichas-medicas/<int:pk>/editar/', views.editar_ficha_medica, name='editar_ficha_medica'),
    path('fichas-medicas/<int:pk>/eliminar/', views.eliminar_ficha_medica, name='eliminar_ficha_medica'),

    path('ventas/', views.lista_ventas, name='listado_ventas'),
    path('ventas/nueva/', views.crear_venta, name='crear_venta'),
    path('ventas/<int:pk>/editar/', views.editar_venta, name='editar_venta'),
    path('ventas/<int:pk>/eliminar/', views.eliminar_venta, name='eliminar_venta'),
]
