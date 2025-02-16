from datetime import datetime

from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import ValidationError, model_to_dict

from config import settings
from core.pos.choices import genders

class Brand(models.Model):
    idBrand = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=100, unique=True, verbose_name="Marca")

    class Meta:
        db_table = "brands"
        ordering = ["brand"]

    def __str__(self):
        return self.brand
    
class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Categoría parent", related_name="subcategories")
    category = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    codigo_base = models.CharField(max_length=15, unique=True, blank=True, verbose_name="Código Base")
    siglas = models.CharField(max_length=10, blank=True, verbose_name="Siglas")

    def save(self, *args, **kwargs):
        if not self.codigo_base:
            self.codigo_base = self.generar_codigo_base()
        self.siglas = self.generar_siglas()
        jerarquia = self.jerarquia()
        
        # Validar duplicados antes de guardar
        if Category.objects.filter(codigo_base=self.codigo_base).exclude(idCategory=self.id).exists():
            raise ValidationError(f"El código base '{self.codigo_base}' ya existe en otra categoría.")
        if Category.objects.filter(siglas=self.siglas).exclude(idCategory=self.id).exists():
            raise ValidationError(f"Las siglas '{self.siglas}' ya existen en otra categoría.")
        if Category.objects.filter(category=jerarquia).exclude(idCategory=self.id).exists():
            raise ValidationError(f"La jerarquía '{jerarquia}' ya existe en otra categoría.")

        super().save(*args, **kwargs)
        
    def generar_codigo_base(self):
        """Genera el código base según la jerarquía de la categoría."""
        if not self.parent:
            # Nivel Abuela (900+)
            base = "900"
        else:
            # Obtener código de la categoría padre
            codigo_padre = self.parent.codigo_base
            nivel_padre = len(codigo_padre)

            if nivel_padre == 3:
                base = codigo_padre + "1"  # Madre (1)
            elif nivel_padre == 4:
                base = codigo_padre + "01"  # Hija (01)
            elif nivel_padre == 6:
                base = codigo_padre + "001"  # Nieta (001)
            else:
                raise ValueError("Error en la jerarquía de la categoría")

        # Asegurarse de que el código base sea único
        while Category.objects.filter(codigo_base=base).exists():
            if not self.parent:
                base = str(int(base) + 1)
            elif nivel_padre == 3:
                base = str(int(base) + 1)
            elif nivel_padre == 4:
                base = codigo_padre + str(int(base[-2:]) + 1).zfill(2)
            elif nivel_padre == 6:
                base = codigo_padre + str(int(base[-3:]) + 1).zfill(3)

        return base

    def generar_siglas(self):
        """Genera las siglas basadas en la jerarquía."""
        siglas = []
        actual = self

        while actual:
            siglas.append(actual.category[:2].upper())  # Tomar las 2 primeras letras de cada nivel
            actual = actual.parent

        return "".join(reversed(siglas))  # Concatenar de nivel más alto a más bajo

    def jerarquia(self):
        jerarquia = []
        actual = self
        while actual:
            jerarquia.append(actual.category)
            actual = actual.parent
        return '-'.join(reversed(jerarquia))
    
    def __str__(self):
        return self.jerarquia()
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']
        db_table = "categories"

class Unit(models.Model):
    idUnit = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=255)

    class Meta:
        db_table = "units"

    def __str__(self):
        return self.unit
    
class Product(models.Model):
    idProduct = models.AutoField(primary_key=True)
    idCategory = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    is_inventoried = models.BooleanField(default=True, verbose_name='¿Es inventariado?')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    idMarca = models.ForeignKey(Brand, on_delete=models.PROTECT)
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True, default="")
    idUnit = models.ForeignKey(Unit, on_delete=models.PROTECT, default=1)   # Unidad de medida
    is_new = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = f'{self.pvp:.2f}'
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-idCategory', 'name', 'idMarca']
        db_table = "products"

    def save(self, *args, **kwargs):
        """Genera el código de barras concatenando codigo_base + consecutivo de 3 dígitos."""
        if not self.barcode:
            last_product = Product.objects.filter(idCategory=self.idCategory).order_by('-barcode').first()
            last_code = int(last_product.barcode[-3:]) + 1 if last_product and last_product.barcode else 1
            self.barcode = f"{self.idCategory.codigo_base}{last_code:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.idCategory.siglas} - {self.barcode}"


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Número de cedula')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=genders, default='male', verbose_name='Genero')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Company(models.Model):
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    ruc = models.CharField(max_length=13, verbose_name='Ruc')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono Celular')
    phone = models.CharField(max_length=7, verbose_name='Teléfono Convencional')
    website = models.CharField(max_length=150, verbose_name='Website')
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can change Company'),
        )
        ordering = ['id']


class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.client.names

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Sale, self).save()

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['client'] = self.client.toJSON()
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.filter(product__is_inventoried=True):
            detail.product.stock += detail.cant
            detail.product.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']
