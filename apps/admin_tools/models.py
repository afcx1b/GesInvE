from django.db import models
from django.forms import model_to_dict
from apps.users.models import User
from conf import settings

class ImportExportLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[("IMPORT", "Importación"), ("EXPORT", "Exportación")])
    table_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


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