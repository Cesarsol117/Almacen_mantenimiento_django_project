from django.db import models

from AppMaquinas.models import Machine

# Create your models here.

class Repuestos(models.Model):
    name_spare_part     = models.CharField(max_length=20, verbose_name='Nombre Repuesto')
    quantity            = models.IntegerField(default=0, verbose_name='Cantidad')
    date_to_register    = models.DateTimeField(auto_now_add=True, editable=True)
    date_to_out         = models.DateTimeField(null=True, blank=True)
    available           = models.BooleanField(null=True)
    
    code                = models.CharField(max_length=50, unique=True, verbose_name='Código del Repuesto')
    storage_location    = models.CharField(max_length=100, verbose_name='Ubicación en Almacén')
    minimum_stock       = models.IntegerField(default=0, verbose_name='Stock Mínimo')
    notes               = models.TextField(blank=True, null=True, verbose_name='Notas Adicionales')
    machines =            models.ManyToManyField(Machine, related_name='repuestos')
    def __str__(self):
        return f'{self.name_spare_part } {self.code} {self.date_to_out} {self.quantity}'

class RegistroEntradasSalidas(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('devoluciones', 'Devoluciones')
    ]
    
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES, null=True)
    cantidad = models.PositiveIntegerField(null=True)
    date_to_movent = models.DateTimeField(auto_now_add=True, null=True)
    machine_relation = models.ManyToManyField(Machine, related_name='maquina_registro')
    spare_part_relation = models.ForeignKey(Repuestos, verbose_name="", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'tipo de salida : {self.tipo_movimiento } cantidad: {self.cantidad}  Maquinas: {self.machine_relation.name} - Repuestos:{self.spare_part_relation.name_spare_part}'
