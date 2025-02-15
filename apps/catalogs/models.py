from django.db import models
from django.utils import timezone
from apps.categories.models import Category
from apps.products.models import Product
from apps.brands.models import Brand
from apps.users.models import Customer, User
from apps.kardex.models import Kardex

class Offer(models.Model):
    # Estado de la oferta (si está activa o no)
    STATUS_CHOICES = [
        ("active", "Activa"),
        ("inactive", "Inactiva"),
    ]

    idOffer = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  # Título de la oferta
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Descuento en porcentaje
    start_date = models.DateTimeField()  # Fecha de inicio de la oferta
    end_date = models.DateTimeField()  # Fecha de finalización de la oferta
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")  # Estado de la oferta
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría asociada
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)  # Producto específico
    is_global = models.BooleanField(default=False)  # Si la oferta es global (aplica a toda la tienda)
    
    class Meta:
        db_table = "offers"

    def __str__(self):
        return self.title

    def is_active(self):
        # Verifica si la oferta está activa según las fechas actuales
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.status == "active"
    
class OfferDetail(models.Model):
    idOfferDetail = models.AutoField(primary_key=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)  # Relaciona con la oferta
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Relaciona con el producto
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2)  # Precio con descuento aplicado

    class Meta:
        db_table = "offer_details"

    def __str__(self):
        return f"Oferta de {self.offer.title} para {self.product.product}"

class Order(models.Model):
    ORDER_TYPES = [
        ("quote", "Cotización"),
        ("purchase", "Compra"),
    ]
    
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("confirmed", "Confirmado"),
        ("cancelled", "Cancelado"),
    ]

    idOrder = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES, default="quote")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Pedido {self.idOrder} - {self.customer}"

class OrderDetail(models.Model):
    idDetail = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_details"

    def __str__(self):
        return f"{self.quantity} x {self.product.product} - Pedido {self.order.idOrder}"

class Banner(models.Model):
    POSITION_CHOICES = [
        ("carousel", "Carrusel"),
        ("section", "Sección fija"),
        ("both", "Ambos"),
    ]

    LAYOUT_CHOICES = [
        ("row", "Fila"),
        ("grid", "Cuadrícula"),
    ]

    idBanner = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="banners/")
    url = models.URLField(null=True, blank=True)  # URL de destino (opcional)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default="carousel")
    layout = models.CharField(max_length=5, choices=LAYOUT_CHOICES, default="row")

    class Meta:
        db_table = "banners"

    def __str__(self):
        return self.title if self.title else "Banner sin título"

class Catalog(models.Model):
    idCatalog = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="catalogs/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalogs"

    def __str__(self):
        return self.title

class CatalogProduct(models.Model):
    idCatalogProduct = models.AutoField(primary_key=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pvp = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Hacer que pvp no sea editable
    added_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "catalog_products"
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} in {self.catalog.title}"

    def apply_discount(self):
        now = timezone.now()
        if (now - self.added_at).days > 30:  # Si el producto lleva más de 30 días en el catálogo
            self.product.discount_percentage = 40.0
            self.product.save()

    def save(self, *args, **kwargs):
        # Obtener el pvp del producto antes de guardar
        self.pvp = self.product.price
        super(CatalogProduct, self).save(*args, **kwargs)