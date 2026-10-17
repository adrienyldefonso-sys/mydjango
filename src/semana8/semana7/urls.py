from django.urls import path

from .views import registrar_venta, reporte

app_name = 'semana7'

urlpatterns = [
    path('semana7/reporte/', reporte, name='reporte'),
    path('semana7/ventas/registrar/', registrar_venta, name='registrar_venta'),
]
