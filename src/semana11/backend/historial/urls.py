from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DiagnosticoViewSet, HistorialParcelaView, ParcelaListView


router = DefaultRouter()
router.register('diagnosticos', DiagnosticoViewSet, basename='diagnostico')

urlpatterns = [
    path('parcelas/', ParcelaListView.as_view(), name='parcela-list'),
    path(
        'parcelas/<uuid:parcela_id>/historial/',
        HistorialParcelaView.as_view(),
        name='parcela-historial',
    ),
] + router.urls
