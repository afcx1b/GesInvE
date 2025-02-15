from django.db import models
from apps.products.models import Product

class Kardex(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    articulo = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Artículo")
    fecha = models.DateField(verbose_name="Fecha de movimiento")
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO, verbose_name="Tipo de movimiento")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio de venta")
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="Costo total")

    def save(self, *args, **kwargs):
        # Calcular el costo total automáticamente
        self.costo_total = self.cantidad * self.costo_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_movimiento.capitalize()} de {self.articulo.nombre} el {self.fecha}"
    
class Costo(models.Model):
    articulo = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Artículo")
    fecha = models.DateField(verbose_name="Fecha de costo")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario")

    def __str__(self):
        return f"Costo de {self.articulo.nombre} el {self.fecha}"

class Precio(models.Model):
    articulo = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Artículo")
    fecha = models.DateField(verbose_name="Fecha de costo")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de venta")

    def __str__(self):
        return f"Precio de {self.articulo.nombre} el {self.fecha}"
    
     