from datetime import date

from django.test import TestCase

from .models import ObjetoEncontrado, Ubicacion


class ObjetoEncontradoModelTests(TestCase):
    def test_crear_y_buscar_objeto(self):
        ubicacion, _ = Ubicacion.objects.get_or_create(nombre='Biblioteca')

        ObjetoEncontrado.objects.create(
            nombre='Mochila negra',
            descripcion='Mochila con cuadernos.',
            ubicacion=ubicacion,
            fecha=date(2026, 8, 25),
            contacto='Ana Torres',
        )

        self.assertGreaterEqual(ObjetoEncontrado.objects.filter(ubicacion=ubicacion).count(), 1)
        self.assertTrue(ObjetoEncontrado.objects.buscar('biblioteca').exists())
        self.assertFalse(ObjetoEncontrado.objects.buscar('colegio-inexistente').exists())

    def test_relacion_uno_a_muchos_entre_ubicacion_y_objeto(self):
        biblioteca, _ = Ubicacion.objects.get_or_create(nombre='Biblioteca')
        patio, _ = Ubicacion.objects.get_or_create(nombre='Patio principal')

        ObjetoEncontrado.objects.create(
            nombre='Lentes de sol',
            descripcion='Lentes con marco dorado.',
            ubicacion=patio,
            fecha=date(2026, 8, 24),
            contacto='Carlos Mendez',
        )

        self.assertGreaterEqual(biblioteca.objetos.count(), 1)
        self.assertGreaterEqual(patio.objetos.count(), 1)
        self.assertGreaterEqual(ObjetoEncontrado.objects.filter(ubicacion=biblioteca).count(), 1)
