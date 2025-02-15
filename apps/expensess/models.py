from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

Usuario = get_user_model()

class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Categoría de Gasto"
        verbose_name_plural = "Categorías de Gastos"

    def __str__(self):
        return self.nombre

class Gasto(models.Model):
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.SET_NULL, null=True, blank=True)
    # ... otros campos ...
    METODOS_PAGO = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
        ('TC', 'Tarjeta de Crédito'),
    ]
    metodo_pago = models.CharField(max_length=2, choices=METODOS_PAGO, default='EF')
    # ... otros campos ...
    
    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return f"{self.descripcion} - ${self.monto}"
