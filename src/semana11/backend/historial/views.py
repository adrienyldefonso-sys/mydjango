from uuid import UUID

from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Diagnostico, Parcela
from .serializers import (
    DiagnosticoSerializer,
    ParcelaHistorialSerializer,
    ParcelaSerializer,
)


class DiagnosticoViewSet(ModelViewSet):
    queryset = Diagnostico.objects.select_related('parcela').all()
    serializer_class = DiagnosticoSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('plaga_nombre', 'plaga_detectada')
    ordering_fields = (
        'fecha_captura',
        'plaga_nombre',
        'plaga_detectada',
        'confianza',
    )
    ordering = ('-fecha_captura',)

    def get_queryset(self):
        queryset = super().get_queryset()
        parcela_id = self.request.query_params.get('parcela')

        if parcela_id:
            try:
                parcela_id = UUID(parcela_id)
            except ValueError as error:
                raise ValidationError({
                    'parcela': 'Usa un UUID válido para identificar la parcela.',
                }) from error
            queryset = queryset.filter(parcela_id=parcela_id)

        plaga_detectada = self.request.query_params.get('plaga_detectada')
        if plaga_detectada:
            queryset = queryset.filter(plaga_detectada=plaga_detectada)

        filtros_fecha = {}
        for parametro, campo in (
            ('desde', 'fecha_captura__date__gte'),
            ('hasta', 'fecha_captura__date__lte'),
        ):
            valor = self.request.query_params.get(parametro)
            if valor:
                fecha = parse_date(valor)
                if fecha is None:
                    raise ValidationError({
                        parametro: 'Usa el formato de fecha YYYY-MM-DD.',
                    })
                filtros_fecha[parametro] = fecha
                queryset = queryset.filter(**{campo: fecha})

        if (
            filtros_fecha.get('desde')
            and filtros_fecha.get('hasta')
            and filtros_fecha['desde'] > filtros_fecha['hasta']
        ):
            raise ValidationError({
                'desde': 'La fecha inicial no puede ser posterior a la fecha final.',
            })

        return queryset


class ParcelaListView(APIView):
    def get(self, request):
        parcelas = Parcela.objects.all()
        return Response(ParcelaSerializer(parcelas, many=True).data)


class HistorialParcelaView(APIView):
    def get(self, request, parcela_id):
        parcela = Parcela.objects.filter(pk=parcela_id).first()
        if parcela is None:
            return Response(
                {'detail': 'No existe la parcela solicitada.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        diagnosticos = Diagnostico.objects.filter(parcela=parcela)
        filtros_fecha = {}

        for parametro in ('desde', 'hasta'):
            valor = request.query_params.get(parametro)
            if valor:
                fecha = parse_date(valor)
                if fecha is None:
                    return Response(
                        {parametro: 'Usa el formato de fecha YYYY-MM-DD.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                filtros_fecha[parametro] = fecha

        if filtros_fecha.get('desde') and filtros_fecha.get('hasta'):
            if filtros_fecha['desde'] > filtros_fecha['hasta']:
                return Response(
                    {'desde': 'La fecha inicial no puede ser posterior a la fecha final.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if 'desde' in filtros_fecha:
            diagnosticos = diagnosticos.filter(
                fecha_captura__date__gte=filtros_fecha['desde'],
            )
        if 'hasta' in filtros_fecha:
            diagnosticos = diagnosticos.filter(
                fecha_captura__date__lte=filtros_fecha['hasta'],
            )

        serializer = ParcelaHistorialSerializer(
            parcela,
            context={'diagnosticos': diagnosticos},
        )
        return Response(serializer.data)
