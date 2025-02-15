from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product
from apps.users.models import User

# Modelo para Ubicaciones
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre de la ubicación (ej: Estante A)", verbose_name="Nombre")
    codigo = models.CharField(max_length=10, unique=True, help_text="Código único de la ubicación (ej: EST-A)", verbose_name="Código")

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
class InventarioInicial(models.Model):
    articulo = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Artículo")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo", blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, verbose_name="Ubicación")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return f"{self.articulo.nombre} - {self.cantidad} unidades"

# Modelo para Movimientos entre Ubicaciones
class MovimientoUbicacion(models.Model):
    articulo = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Artículo")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    ubicacion_origen = models.ForeignKey(Ubicacion, related_name='movimientos_origen', on_delete=models.CASCADE, verbose_name="Ubicación de origen")
    ubicacion_destino = models.ForeignKey(Ubicacion, related_name='movimientos_destino', on_delete=models.CASCADE, verbose_name="Ubicación de destino")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return f"{self.articulo.nombre} - {self.cantidad} unidades"

# Modelo para Dar de Baja Artículos
class BajaArticulo(models.Model):
    articulo = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Artículo")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    motivo = models.TextField(verbose_name="Motivo")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return f"{self.articulo.nombre} - {self.cantidad} unidades"

class Inventario(models.Model):
    articulo = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Artículo", unique=True)
    cantidad_disponible = models.PositiveIntegerField(default=0, verbose_name="Cantidad disponible")

    def __str__(self):
        return f"Inventario de {self.articulo.nombre}: {self.cantidad_disponible} unidades"