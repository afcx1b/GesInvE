from django.db import models
from django.core.exceptions import ValidationError
 
class Category(models.Model):
    idCategory = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, verbose_name="Categoría")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Categoría parent", related_name="subcategories")
    codigo_base = models.CharField(max_length=15, unique=True, blank=True, verbose_name="Código Base")
    siglas = models.CharField(max_length=10, blank=True, verbose_name="Siglas")
    #fecha_creacion = models.DateTimeField(auto_now_add=True)
     
    class Meta:
        db_table = "categories"
        ordering = ['-idCategory']
 
    def save(self, *args, **kwargs):
        if not self.codigo_base:
            self.codigo_base = self.generar_codigo_base()
        self.siglas = self.generar_siglas()
        jerarquia = self.jerarquia()
        
        # Validar duplicados antes de guardar
        if Category.objects.filter(codigo_base=self.codigo_base).exclude(idCategory=self.idCategory).exists():
            raise ValidationError(f"El código base '{self.codigo_base}' ya existe en otra categoría.")
        if Category.objects.filter(siglas=self.siglas).exclude(idCategory=self.idCategory).exists():
            raise ValidationError(f"Las siglas '{self.siglas}' ya existen en otra categoría.")
        if Category.objects.filter(category=jerarquia).exclude(idCategory=self.idCategory).exists():
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

    def __str__(self):
        return f"{self.category} - {self.codigo_base} - {self.siglas}"

    def jerarquia(self):
        jerarquia = []
        actual = self
        while actual:
            jerarquia.append(actual.category)
            actual = actual.parent
        return '-'.join(reversed(jerarquia))

    def __str__(self):
        return self.jerarquia()