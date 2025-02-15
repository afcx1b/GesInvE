import os
from django.db import models

class Brand(models.Model):
    idBrand = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=100, unique=True, verbose_name="Marca")

    class Meta:
        db_table = "brands"
        ordering = ["brand"]

    def __str__(self):
        return self.brand
