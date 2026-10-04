from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from semana5.models import Cliente, Producto, Venta
from .models import ClienteReporte


class RegistrarVentaTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres='Cliente',
            apellidos='Prueba',
            dni='TEST-VENTA-01',
        )
        self.producto = Producto.objects.create(
            nombre='Producto de prueba',
            tipo='armazon',
            precio=Decimal('25.00'),
            stock=5,
        )
        self.url = reverse('semana7:registrar_venta')

    def test_successful_sale_reduces_stock_and_creates_sale(self):
        response = self.client.post(self.url, {
            'cliente_id': self.cliente.pk,
            'producto_id': self.producto.pk,
            'cantidad': 2,
        }, follow=True)

        self.producto.refresh_from_db()
        venta = Venta.objects.get(cliente=self.cliente, producto=self.producto)

        self.assertEqual(self.producto.stock, 3)
        self.assertEqual(venta.cantidad, 2)
        self.assertEqual(venta.precio_unitario, Decimal('25.00'))
        self.assertEqual(venta.estado, 'pendiente')
        self.assertContains(response, 'Venta registrada correctamente.')
        self.assertTemplateUsed(response, 'semana7/registrar_venta.html')

    def test_sale_creation_failure_rolls_back_stock_update(self):
        with patch(
            'semana7.views.Venta.objects.create',
            side_effect=IntegrityError('Fallo de persistencia simulado.'),
        ):
            response = self.client.post(self.url, {
                'cliente_id': self.cliente.pk,
                'producto_id': self.producto.pk,
                'cantidad': 2,
            }, follow=True)

        self.producto.refresh_from_db()

        self.assertEqual(self.producto.stock, 5)
        self.assertFalse(Venta.objects.filter(producto=self.producto).exists())
        self.assertContains(response, 'No se pudo registrar la venta:')
        self.assertTemplateUsed(response, 'semana7/registrar_venta.html')


class ReporteVentasTests(TestCase):
    def test_aggregate_and_annotate_reports_are_rendered(self):
        cliente = Cliente.objects.create(
            nombres='Reporte',
            apellidos='Prueba',
            dni='TEST-REPORTE-01',
        )
        producto_a = Producto.objects.create(
            nombre='Producto A',
            tipo='armazon',
            precio=Decimal('10.00'),
            stock=5,
        )
        producto_b = Producto.objects.create(
            nombre='Producto B',
            tipo='luna',
            precio=Decimal('15.00'),
            stock=5,
        )
        Venta.objects.create(
            cliente=cliente,
            producto=producto_a,
            fecha_venta=date.today(),
            cantidad=2,
            precio_unitario=Decimal('10.00'),
            estado='pendiente',
        )
        Venta.objects.create(
            cliente=cliente,
            producto=producto_b,
            fecha_venta=date.today(),
            cantidad=1,
            precio_unitario=Decimal('15.00'),
            estado='pagado',
        )

        with self.assertNumQueries(4):
            response = self.client.get(reverse('semana7:reporte'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'semana7/reporte.html')
        self.assertEqual(response.context['total'], Decimal('35.00'))
        self.assertContains(response, '35.00')

        clientes_reportados = list(response.context['clientes_con_ventas'])
        self.assertEqual(clientes_reportados[0].num_ventas, 2)
        self.assertContains(response, 'Reporte Prueba')

        ventas_por_estado = {
            fila['estado']: fila['total']
            for fila in response.context['ventas_por_estado']
        }
        self.assertEqual(ventas_por_estado, {'pendiente': 1, 'pagado': 1})
        self.assertContains(response, 'Ventas por estado')


class ClienteQuerySetTests(TestCase):
    def setUp(self):
        self.cliente_pendiente = Cliente.objects.create(
            nombres='Pendiente',
            apellidos='QuerySet',
            dni='TEST-QS-01',
        )
        self.cliente_pagado = Cliente.objects.create(
            nombres='Pagado',
            apellidos='QuerySet',
            dni='TEST-QS-02',
        )
        producto = Producto.objects.create(
            nombre='Producto QuerySet',
            tipo='armazon',
            precio=Decimal('12.00'),
            stock=5,
        )
        for cliente, estado in (
            (self.cliente_pendiente, 'pendiente'),
            (self.cliente_pagado, 'pagado'),
        ):
            Venta.objects.create(
                cliente=cliente,
                producto=producto,
                fecha_venta=timezone.localdate(),
                cantidad=1,
                precio_unitario=Decimal('12.00'),
                estado=estado,
            )

    def test_custom_queryset_methods_are_chainable(self):
        pendientes = ClienteReporte.objects.con_ventas_pendientes().filter(
            pk=self.cliente_pendiente.pk
        ).order_by('dni')
        del_mes = ClienteReporte.objects.del_mes_actual().filter(
            pk=self.cliente_pagado.pk
        ).order_by('dni')

        self.assertEqual(list(pendientes), [self.cliente_pendiente])
        self.assertEqual(list(del_mes), [self.cliente_pagado])

    def test_two_week7_views_use_custom_queryset_methods(self):
        pendientes = self.client.get(reverse('semana7:registrar_venta'))
        del_mes = self.client.get(reverse('semana7:reporte'))

        self.assertEqual(pendientes.status_code, 200)
        self.assertContains(pendientes, 'Pendiente QuerySet')
        self.assertEqual(
            list(pendientes.context['clientes_pendientes'].values_list('pk', flat=True)),
            [self.cliente_pendiente.pk],
        )
        self.assertEqual(del_mes.status_code, 200)
        self.assertContains(del_mes, 'Pendiente QuerySet')
        self.assertContains(del_mes, 'Pagado QuerySet')
        self.assertEqual(
            {cliente.pk for cliente in del_mes.context['clientes_mes']},
            {self.cliente_pendiente.pk, self.cliente_pagado.pk},
        )