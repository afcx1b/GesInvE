from django.db import models
from apps.users.models import User

# Modelo para Reportes
class Reporte(models.Model):
    TIPOS_REPORTE = (
        ('COMPRAS', 'Compras'),
        ('VENTAS', 'Ventas'),
        ('GASTOS', 'Gastos'),
        ('COMISIONES', 'Comisiones'),
    )

    tipo = models.CharField(max_length=10, choices=TIPOS_REPORTE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.fecha_inicio} a {self.fecha_fin}"