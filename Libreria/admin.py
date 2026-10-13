from django.contrib import admin
from .models import Editorial, Libro


def _formatear_pesos_chilenos(monto):
    return f'${monto:,.0f}'.replace(',', '.')


admin.site.site_header = 'Administración de la librería'
admin.site.site_title = 'Administración de la librería'
admin.site.index_title = 'Gestión de editoriales y libros'


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'direccion',
        'telefono',
        'correo_electronico',
        'mostrar_monto_asignado',
    )
    list_filter = ('monto_asignado_pesos',)
    search_fields = ('nombre', 'direccion', 'telefono', 'correo_electronico')

    @admin.display(description='Monto asignado (CLP)', ordering='monto_asignado_pesos')
    def mostrar_monto_asignado(self, editorial):
        return _formatear_pesos_chilenos(editorial.monto_asignado_pesos)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'autor',
        'isbn',
        'editorial',
        'fecha_publicacion',
        'mostrar_precio',
    )
    list_filter = ('editorial', 'fecha_publicacion')
    search_fields = ('titulo', 'autor', 'isbn', 'editorial__nombre')

    @admin.display(description='Precio (CLP)', ordering='precio_pesos')
    def mostrar_precio(self, libro):
        return _formatear_pesos_chilenos(libro.precio_pesos)
