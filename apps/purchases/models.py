from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

Usuario = get_user_model()

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # ... otros campos ...
    METODOS_PAGO = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
        ('TC', 'Tarjeta de Crédito'),
    ]
    metodo_pago = models.CharField(max_length=2, choices=METODOS_PAGO, default='EF')
    # ... otros campos ...
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra #{self.id} - {self.proveedor.nombre}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    articulo = models.ForeignKey(Product, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compra"

    def __str__(self):
        return f"{self.articulo.nombre} - {self.cantidad} unidades"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.compra.total = sum(item.cantidad * item.costo for item in self.compra.detalles.all())
        self.compra.save()
