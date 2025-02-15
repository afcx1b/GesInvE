from django.db import models
from apps.users.models import User

# Modelo para Configuraciones Generales
class ConfiguracionGeneral(models.Model):
    nombre_sistema = models.CharField(max_length=100, default="Sistema de Inventario")
    logo = models.ImageField(upload_to='configuraciones/', blank=True, null=True)
    moneda = models.CharField(max_length=10, default="USD")
    impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=17.00, verbose_name="Impuesto IVA")
    precio1 = models.DecimalField(max_digits=5, decimal_places=2, default=50.00, verbose_name="Precio Venta Publico")
    precio2 = models.DecimalField(max_digits=5, decimal_places=2, default=35.00, verbose_name="Precio Venta Mayorista")
    precio3 = models.DecimalField(max_digits=5, decimal_places=2, default=25.00, verbose_name="Precio Venta Distribuidor")

    def __str__(self):
        return self.nombre_sistema

        return self.state

class Unit(models.Model):
    idUnit = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=255)

    class Meta:
        db_table = "units"

    def __str__(self):
        return self.unit

class Cashier(models.Model):
    idCashier = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cashier = models.CharField(max_length=255)
    serialNumber = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "cashiers"

    def __str__(self):
        return self.cashier

