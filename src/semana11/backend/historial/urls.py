from django.urls import path

from .views import HistorialParcelaView, ParcelaListView


urlpatterns = [
    path('parcelas/', ParcelaListView.as_view(), name='parcela-list'),
    path(
        'parcelas/<uuid:parcela_id>/historial/',
        HistorialParcelaView.as_view(),
        name='parcela-historial',
    ),
]
