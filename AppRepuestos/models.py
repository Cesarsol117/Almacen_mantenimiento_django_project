from django.db import models

from AppMaquinas.models import Machine

# Create your models here.

class Repuestos(models.Model):
    name_spare_part     = models.CharField(max_length=20, verbose_name='Nombre Repuesto')
    quantity            = models.IntegerField(default=0, verbose_name='Cantidad')
    date_to_register    = models.DateTimeField(auto_now_add=True, editable=True)
    date_to_out         = models.DateField(auto_now=True)
    available           = models.BooleanField(null=True)
    
    code                = models.CharField(max_length=50, unique=True, verbose_name='Código del Repuesto')
    storage_location    = models.CharField(max_length=100, verbose_name='Ubicación en Almacén')
    minimum_stock       = models.IntegerField(default=0, verbose_name='Stock Mínimo')
    notes               = models.TextField(blank=True, null=True, verbose_name='Notas Adicionales')
    machines =            models.ManyToManyField(Machine, related_name='repuestos')
    def __str__(self):
        return f'{self.name_spare_part }+ [{self.code}]'