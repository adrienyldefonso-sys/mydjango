from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Diagnostico, Parcela
from .serializers import ParcelaHistorialSerializer, ParcelaSerializer


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
