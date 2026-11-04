from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Diagnostico, Parcela
from .serializers import DiagnosticoSerializer


class HistorialModelTests(TestCase):
    def setUp(self):
        self.parcela = Parcela.objects.create(
            id=uuid4(),
            nombre='Chacra Los Andes',
            cultivo='Papa',
            referencia='Huarochirí',
            latitud=Decimal('-12.130000'),
            longitud=Decimal('-76.230000'),
            agricultor='Luis Quispe',
        )

    def test_diagnostico_belongs_to_parcela_and_increments_count(self):
        diagnostico = Diagnostico.objects.create(
            parcela=self.parcela,
            fecha_captura=timezone.make_aware(datetime(2026, 10, 30, 16, 36)),
            plaga_detectada='Potato___Late_blight',
            plaga_nombre='Tizón Tardío',
            confianza=Decimal('92.10'),
            imagen_url='https://example.com/papa.jpg',
        )

        self.assertEqual(diagnostico.parcela, self.parcela)
        self.assertEqual(self.parcela.total_diagnosticos, 1)
        self.assertEqual(self.parcela.diagnosticos.first(), diagnostico)

    def test_confidence_must_be_between_zero_and_one_hundred(self):
        diagnostico = Diagnostico(
            parcela=self.parcela,
            fecha_captura=timezone.now(),
            plaga_detectada='Potato___healthy',
            plaga_nombre='Saludable',
            confianza=Decimal('100.01'),
        )

        with self.assertRaises(ValidationError):
            diagnostico.full_clean()


class HistorialApiTests(APITestCase):
    def setUp(self):
        self.parcela = Parcela.objects.create(
            nombre='Chacra Los Andes',
            cultivo='Papa',
            referencia='Huarochirí',
            latitud=Decimal('-12.130000'),
            longitud=Decimal('-76.230000'),
            agricultor='Luis Quispe',
        )
        Diagnostico.objects.create(
            parcela=self.parcela,
            fecha_captura=timezone.make_aware(datetime(2026, 10, 30, 16, 36)),
            plaga_detectada='Potato___Late_blight',
            plaga_nombre='Tizón Tardío',
            confianza=Decimal('92.10'),
        )

    def test_historial_serializes_parcela_summary_and_related_diagnoses(self):
        response = self.client.get(f'/api/parcelas/{self.parcela.id}/historial/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['parcela']['nombre'], 'Chacra Los Andes')
        self.assertEqual(response.data['resumen']['total'], 1)
        self.assertEqual(response.data['resumen']['por_plaga'], {'Potato___Late_blight': 1})
        self.assertEqual(len(response.data['diagnosticos']), 1)

    def test_historial_rejects_invalid_date_range(self):
        response = self.client.get(
            f'/api/parcelas/{self.parcela.id}/historial/?desde=2026-10-31&hasta=2026-10-01',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('desde', response.data)

    def test_serializer_rejects_confidence_above_one_hundred(self):
        serializer = DiagnosticoSerializer(data={
            'parcela': str(self.parcela.id),
            'fecha_captura': '2026-10-30T16:36:00-05:00',
            'plaga_detectada': 'Potato___healthy',
            'plaga_nombre': 'Saludable',
            'confianza': '100.01',
            'imagen_url': '',
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('confianza', serializer.errors)
