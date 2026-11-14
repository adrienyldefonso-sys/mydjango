from django.db.models import Count, QuerySet
from rest_framework import serializers

from .models import Diagnostico, Parcela


class ParcelaSerializer(serializers.ModelSerializer):
    total_diagnosticos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Parcela
        fields = (
            'id',
            'nombre',
            'cultivo',
            'referencia',
            'latitud',
            'longitud',
            'agricultor',
            'total_diagnosticos',
        )


class DiagnosticoSerializer(serializers.ModelSerializer):
    confianza = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate_confianza(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                'La confianza debe estar entre 0 y 100.',
            )
        return value

    class Meta:
        model = Diagnostico
        fields = (
            'id',
            'parcela',
            'fecha_captura',
            'plaga_detectada',
            'plaga_nombre',
            'confianza',
            'imagen_url',
        )


class DiagnosticoHistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = (
            'id',
            'fecha_captura',
            'plaga_detectada',
            'plaga_nombre',
            'confianza',
            'imagen_url',
        )


class ParcelaHistorialSerializer(serializers.Serializer):
    parcela = serializers.SerializerMethodField()
    resumen = serializers.SerializerMethodField()
    diagnosticos = serializers.SerializerMethodField()

    def get_parcela(self, instance):
        return ParcelaSerializer(instance).data

    def get_diagnosticos_queryset(self, instance) -> QuerySet[Diagnostico]:
        return self.context.get('diagnosticos', instance.diagnosticos.all())

    def get_diagnosticos(self, instance):
        queryset = self.get_diagnosticos_queryset(instance)
        return DiagnosticoHistorialSerializer(queryset, many=True).data

    def get_resumen(self, instance):
        diagnosticos = self.get_diagnosticos_queryset(instance)
        agrupados = {
            item['plaga_detectada']: item['cantidad']
            for item in diagnosticos.values('plaga_detectada')
            .order_by()
            .annotate(cantidad=Count('pk'))
        }

        ultima_fecha = diagnosticos.order_by('-fecha_captura').values_list(
            'fecha_captura',
            flat=True,
        ).first()

        return {
            'total': diagnosticos.count(),
            'ultima_fecha': ultima_fecha,
            'por_plaga': agrupados,
        }
