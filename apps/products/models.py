from django.db import models
from apps.categories.models import Category
from apps.cashier.models import Unit
from apps.brands.models import Brand
import os

def product_image_upload_path(instance, filename):
    """Genera la ruta para guardar la imagen del producto."""
    ext = filename.split('.')[-1]
    filename = f"{instance.idCategory.codigo_base}_{instance.product}.{ext}"
    return os.path.join('products/', filename)

class Product(models.Model):
    idProduct = models.AutoField(primary_key=True)
    idCategory = models.ForeignKey(Category, on_delete=models.PROTECT)
    idMarca = models.ForeignKey(Brand, on_delete=models.PROTECT)
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True, default="")
    product = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)
    idUnit = models.ForeignKey(Unit, on_delete=models.PROTECT, default=1)   # Unidad de medida
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo unitario")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stock = models.PositiveIntegerField(verbose_name="Stock")
    is_new = models.BooleanField(default=False)

    class Meta:
        db_table = "products"
        ordering = ['-idCategory', 'product', 'idMarca']

    def save(self, *args, **kwargs):
        """Genera el código de barras concatenando codigo_base + consecutivo de 3 dígitos."""
        if not self.barcode:
            last_product = Product.objects.filter(idCategory=self.idCategory).order_by('-barcode').first()
            last_code = int(last_product.barcode[-3:]) + 1 if last_product and last_product.barcode else 1
            self.barcode = f"{self.idCategory.codigo_base}{last_code:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.idCategory.siglas} - {self.barcode}"

