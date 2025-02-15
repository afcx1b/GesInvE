from django.utils import timezone
from django.db import models
from apps.products.models import Product
from apps.users.models import User

# Modelo para Clientes (con integración de redes sociales)
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    facebook = models.URLField(blank=True, null=True, verbose_name="Perfil de Facebook")
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name="Usuario de Instagram")
    whatsapp = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número de WhatsApp")
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

# Modelo para manejar consecutivos de Venta, Ticket y Factura
class ConsecutivoVenta(models.Model):
    TIPO_CHOICES = [
        ('VENTA', 'Venta'),
        ('TICKET', 'Ticket'),
        ('FACTURA', 'Factura')
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, unique=True)
    numero_actual = models.PositiveIntegerField(default=0)
    numero_inicial = models.PositiveIntegerField(default=1)
    codigo_autorizacion = models.CharField(max_length=20, blank=True, null=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)

    def incrementar(self):
        self.numero_actual += 1
        self.save()
        return self.numero_actual

    def __str__(self):
        return f"{self.tipo}: {self.numero_actual}"

# Modelo para Venta
class Sale(models.Model):
    venta_id = models.AutoField(primary_key=True)    
    
    TIPO_VENTA = (
        ('TICKET', 'Ticket'),
        ('FACTURA', 'Factura'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo = models.CharField(max_length=10, choices=TIPO_VENTA)
    consecutivo = models.PositiveIntegerField(unique=True, editable=False)
    # ... otros campos ...
    METODOS_PAGO = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
        ('TC', 'Tarjeta de Crédito'),
    ]
    metodo_pago = models.CharField(max_length=2, choices=METODOS_PAGO, default='EF')
    # ... otros campos ...
    
    def save(self, *args, **kwargs):
        if not self.consecutivo:
            consecutivo_venta = ConsecutivoVenta.objects.get(tipo=self.tipo)
            self.consecutivo = consecutivo_venta.incrementar()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} #{self.consecutivo} - {self.cliente.nombre}"

# Modelo para Detalles de Venta
class SaleProduct(models.Model):
    TIPO_PRECIO = (
        ('MINORISTA', 'Minorista'),
        ('MAYORISTA', 'Mayorista'),
        ('PROMOCION', 'Promoción'),
    )
    venta = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='detalles')
    articulo = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_precio = models.CharField(max_length=10, choices=TIPO_PRECIO)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.precio_original = self.articulo.inventarioinicial.costo
        super().save(*args, **kwargs)
        self.venta.total += self.cantidad * self.precio
        self.venta.save()

    def __str__(self):
        return f"{self.articulo.nombre} - {self.cantidad} unidades"

# Modelo para Historial de Precios de Venta
class PrecioVenta(models.Model):
    TIPO_PRECIO = (
        ('MINORISTA', 'Minorista'),
        ('MAYORISTA', 'Mayorista'),
        ('PROMOCION', 'Promoción'),
    )
    articulo = models.ForeignKey(Product, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_PRECIO)
    porcentaje_aumento = models.DecimalField(max_digits=5, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.precio = self.articulo.inventarioinicial.costo * (1 + self.porcentaje_aumento / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.articulo.nombre} - {self.tipo}"

# Modelo para Comisiones por Vendedor
class ComisionVendedor(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    porcentaje_comision = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.vendedor.username} - {self.porcentaje_comision}%"


# Modelo para Tickets
class Ticket(Sale):
    consecutivoT = models.PositiveIntegerField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.consecutivoT:
            consecutivoT = ConsecutivoTicket.objects.first()
            if not consecutivoT:
                consecutivoT = ConsecutivoTicket.objects.create(ultimo_numero=0)
            consecutivoT.ultimo_numero += 1
            self.consecutivo = consecutivoT.ultimo_numero
            consecutivoT.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket #{self.consecutivoT}"


# Modelo para Facturas (cumple con regulación ecuatoriana)
class Factura(Sale):
    consecutivoF = models.PositiveIntegerField(unique=True, editable=False)
    codigo_autorizacion = models.CharField(max_length=20)
    fecha_autorizacion = models.DateField()

    def save(self, *args, **kwargs):
        if not self.consecutivoF:
            consecutivoF = ConsecutivoFactura.objects.first()
            if not consecutivoF:
                consecutivoF = ConsecutivoFactura.objects.create(
                    ultimo_numero=0,
                    codigo_autorizacion="0000000000",
                    fecha_autorizacion="2023-01-01"
                )
            consecutivoF.ultimo_numero += 1
            self.consecutivoF = consecutivoF.ultimo_numero
            self.codigo_autorizacion = consecutivoF.codigo_autorizacion
            self.fecha_autorizacion = consecutivoF.fecha_autorizacion
            consecutivoF.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Factura #{self.consecutivoF}"

# Modelo para Consecutivos de Tickets
class ConsecutivoTicket(models.Model):
    ultimo_numero = models.PositiveIntegerField(default=0)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"Ticket: {self.ultimo_numero}"


# Modelo para Consecutivos de Facturas (según regulación ecuatoriana)
class ConsecutivoFactura(models.Model):
    ultimo_numero = models.PositiveIntegerField(default=0)
    codigo_autorizacion = models.CharField(max_length=20)
    fecha_autorizacion = models.DateField()
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"Factura: {self.ultimo_numero}"
