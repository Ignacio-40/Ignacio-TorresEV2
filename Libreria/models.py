from django.db import models


class Editorial(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    direccion = models.CharField('Dirección', max_length=255, blank=True, default='')
    telefono = models.CharField('Teléfono', max_length=30, blank=True, default='')
    correo_electronico = models.EmailField(
        'Correo electrónico',
        blank=True,
        default='',
    )
    monto_asignado_pesos = models.DecimalField(
        'Monto asignado (pesos)',
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        verbose_name = 'editorial'
        verbose_name_plural = 'editoriales'

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField('Título', max_length=200)
    autor = models.CharField('Autor', max_length=200, blank=True, default='')
    isbn = models.CharField('ISBN', max_length=20, blank=True, default='')
    fecha_publicacion = models.DateField('Fecha de publicación', null=True, blank=True)
    precio_pesos = models.DecimalField(
        'Precio (pesos)',
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    editorial = models.ForeignKey(
        Editorial,
        verbose_name='Editorial',
        on_delete=models.CASCADE,
        related_name='libros',
    )

    class Meta:
        verbose_name = 'libro'
        verbose_name_plural = 'libros'

    def __str__(self):
        return self.titulo
