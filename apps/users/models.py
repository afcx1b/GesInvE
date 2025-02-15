from django.utils import timezone
import json
import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from crum import get_current_request

from conf import settings

def default_permissions():
    file_path = os.path.join(settings.BASE_DIR, "static", "json", "permissions.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}  # Si no se encuentra el archivo, devuelve un diccionario vacío
    
class Position(models.Model):
    idPosition = models.AutoField(primary_key=True)
    position = models.CharField(max_length=255, unique=True, verbose_name="Cargo")
    permissions = models.JSONField(default=default_permissions, verbose_name="Permisos")

    class Meta:
        db_table = "positions"

    def __str__(self):
        return self.position
    
class Employee(models.Model):
    idEmployee = models.AutoField(primary_key=True)
    idPosition = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name="Cargo")
    dni = models.CharField(max_length=13, unique=True, verbose_name="Cédula")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    surname = models.CharField(max_length=255, verbose_name="Apellido")
    phone = models.CharField(max_length=13, verbose_name="Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    address = models.CharField(max_length=255, verbose_name="Dirección")

    class Meta:
        db_table = "employees"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def get_full_name(self):
        return f"{self.name} {self.surname}"
    
class User(AbstractUser):
    idUser = models.AutoField(primary_key=True)
    idEmployee = models.OneToOneField(Employee, on_delete=models.PROTECT, verbose_name="Empleado", null=True, blank=True)  # Permitir nulo y en blanco
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        item['last_login'] = '' if self.last_login is None else self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass

class Customer(models.Model):
    idCustomer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nombre")
    surname = models.CharField(max_length=255, verbose_name="Apellido")
    phone = models.CharField(max_length=13, verbose_name="Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    address = models.CharField(max_length=255, verbose_name="Dirección")

    class Meta:
        db_table = "customers"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def get_full_name(self):
        return f"{self.name} {self.surname}"