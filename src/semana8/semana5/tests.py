from rest_framework import status
from rest_framework.test import APITestCase

from .models import Cliente, FichaMedica


class InvestigacionApiStatusCodeTests(APITestCase):
    # Rutas propias de la Parte 2, separadas de los endpoints de la Parte 1.
    productos_url = '/optica-v3/api/investigacion/productos/'
    clientes_url = '/optica-v3/api/investigacion/clientes/'

    def test_crud_productos_devuelve_codigos_esperados(self):
        # GET de ambos recursos: la lista debe estar disponible sin datos iniciales.
        self.assertEqual(self.client.get(self.productos_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(self.clientes_url).status_code, status.HTTP_200_OK)

        # POST válido: debe crear el producto y devolver su representación.
        valid_response = self.client.post(
            self.productos_url,
            {
                'nombre': 'Producto API de prueba',
                'tipo': 'armazon',
                'marca': 'OpticaTest',
                'precio': '125.00',
                'stock': 3,
            },
            format='json',
        )
        self.assertEqual(valid_response.status_code, status.HTTP_201_CREATED)
        product_url = f'{self.productos_url}{valid_response.data["id"]}/'

        # GET de detalle confirma la lectura y una PK inexistente devuelve 404.
        self.assertEqual(self.client.get(product_url).status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.get(f'{self.productos_url}999999/').status_code,
            status.HTTP_404_NOT_FOUND,
        )

        # POST inválido confirma que el serializer rechaza precios no positivos.
        invalid_response = self.client.post(
            self.productos_url,
            {
                'nombre': 'Producto API inválido',
                'tipo': 'luna',
                'marca': 'OpticaTest',
                'precio': '0.00',
                'stock': 1,
            },
            format='json',
        )
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('precio', invalid_response.data)

        # DELETE elimina solo el producto temporal y responde sin contenido.
        self.assertEqual(self.client.delete(product_url).status_code, status.HTTP_204_NO_CONTENT)


class FichaMedicaReadOnlyApiTests(APITestCase):
    # Endpoint de solo lectura con Cliente anidado.
    fichas_url = '/optica-v3/api/investigacion/fichas-medicas/'

    def test_ficha_medica_muestra_cliente_anidado_y_es_solo_lectura(self):
        cliente = Cliente.objects.create(
            nombres='Cliente',
            apellidos='De prueba',
            dni='TEST-FICHA-001',
        )
        ficha = FichaMedica.objects.create(
            cliente=cliente,
            alergias='Ninguna',
            tipo_seguro='Particular',
        )

        response = self.client.get(self.fichas_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ficha_data = next(item for item in response.data if item['id'] == ficha.id)
        self.assertEqual(ficha_data['cliente']['dni'], cliente.dni)
        self.assertEqual(
            self.client.post(self.fichas_url, {}, format='json').status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class InvestigacionFilterAndActionTests(APITestCase):
    productos_url = '/optica-v3/api/investigacion/productos/'
    clientes_url = '/optica-v3/api/investigacion/clientes/'

    def setUp(self):
        from .models import Cliente, Producto, Venta
        from datetime import date

        self.producto_luna = Producto.objects.create(
            nombre='Luna filtro API',
            tipo='luna',
            marca='MarcaFiltro',
            precio='180.00',
            stock=5,
        )
        Producto.objects.create(
            nombre='Armazon filtro API',
            tipo='armazon',
            marca='MarcaFiltro',
            precio='100.00',
            stock=8,
        )
        cliente = Cliente.objects.create(
            nombres='Cliente',
            apellidos='Pendiente',
            dni='TEST-FILTRO-001',
        )
        Venta.objects.create(
            cliente=cliente,
            producto=self.producto_luna,
            fecha_venta=date(2026, 10, 1),
            cantidad=1,
            precio_unitario='180.00',
            estado='pendiente',
        )

    def test_tipo_search_ordering_y_accion_personalizada(self):
        # Filtro ?tipo= limita productos a un tipo de la investigación.
        tipo_response = self.client.get(self.productos_url, {'tipo': 'luna'})
        self.assertEqual(tipo_response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['tipo'] == 'luna' for item in tipo_response.data))

        # Search y ordering se procesan junto con el filtro ?tipo=.
        combined_response = self.client.get(
            self.productos_url,
            {'tipo': 'luna', 'search': 'Luna', 'ordering': '-precio'},
        )
        self.assertEqual(combined_response.status_code, status.HTTP_200_OK)
        self.assertEqual(combined_response.data[0]['nombre'], 'Luna filtro API')

        # La acción debe incluir el cliente cuya venta está pendiente.
        action_response = self.client.get(
            f'{self.clientes_url}con-ventas-pendientes/'
        )
        self.assertEqual(action_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(item['dni'] == 'TEST-FILTRO-001' for item in action_response.data)
        )
