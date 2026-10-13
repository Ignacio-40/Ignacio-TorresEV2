from decimal import Decimal

from django.contrib import admin
from django.test import TestCase

from .models import Editorial, Libro


class LibroEditorialTests(TestCase):
    def test_libro_se_asocia_a_editorial(self):
        editorial = Editorial.objects.create(nombre='Editorial de prueba')
        libro = Libro.objects.create(titulo='Libro de prueba', editorial=editorial)

        self.assertEqual(libro.editorial, editorial)
        self.assertEqual(list(editorial.libros.all()), [libro])
        self.assertEqual(str(editorial), 'Editorial de prueba')
        self.assertEqual(str(libro), 'Libro de prueba')

    def test_eliminar_editorial_elimina_sus_libros(self):
        editorial = Editorial.objects.create(nombre='Editorial de prueba')
        Libro.objects.create(titulo='Libro de prueba', editorial=editorial)

        editorial.delete()

        self.assertEqual(Libro.objects.count(), 0)

    def test_entidades_guardan_montos_en_pesos(self):
        editorial = Editorial.objects.create(
            nombre='Editorial de prueba',
            monto_asignado_pesos=Decimal('125000.50'),
        )
        libro = Libro.objects.create(
            titulo='Libro de prueba',
            editorial=editorial,
            precio_pesos=Decimal('9500.00'),
        )

        self.assertEqual(editorial.monto_asignado_pesos, Decimal('125000.50'))
        self.assertEqual(libro.precio_pesos, Decimal('9500.00'))

    def test_modelos_estan_registrados_en_admin(self):
        self.assertIn(Editorial, admin.site._registry)
        self.assertIn(Libro, admin.site._registry)
        self.assertEqual(Editorial._meta.verbose_name_plural, 'editoriales')
        self.assertEqual(Libro._meta.verbose_name_plural, 'libros')
        self.assertEqual(admin.site.site_header, 'Administración de la librería')

    def test_listados_del_admin_tienen_columnas_filtros_y_busqueda(self):
        editorial_admin = admin.site._registry[Editorial]
        libro_admin = admin.site._registry[Libro]

        self.assertGreaterEqual(len(editorial_admin.list_display), 3)
        self.assertTrue(editorial_admin.list_filter)
        self.assertTrue(editorial_admin.search_fields)
        self.assertGreaterEqual(len(libro_admin.list_display), 3)
        self.assertTrue(libro_admin.list_filter)
        self.assertTrue(libro_admin.search_fields)

    def test_montos_se_muestran_en_formato_de_pesos_chilenos(self):
        editorial = Editorial(monto_asignado_pesos=Decimal('12990.00'))
        libro = Libro(precio_pesos=Decimal('12990.00'))
        editorial_admin = admin.site._registry[Editorial]
        libro_admin = admin.site._registry[Libro]

        self.assertEqual(editorial_admin.mostrar_monto_asignado(editorial), '$12.990')
        self.assertEqual(libro_admin.mostrar_precio(libro), '$12.990')
