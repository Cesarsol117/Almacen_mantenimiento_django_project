from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.


class Insumos(models.Model):
    TIPO_MEDIDAS_CHOICES = [
        ('g', 'Gramos'),
        ('m', 'Metros'),
        ('und', 'Unidades'),
        ('L', 'litros')
    ]
    nombre = models.CharField(max_length = 50, )
    codigo_insumo = models.CharField(unique=True, max_length=20 )
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(0)], )
    unidad_medida = models.CharField(choices=TIPO_MEDIDAS_CHOICES, max_length=50, )
    disponible = models.BooleanField(default=True, )
    stock_minimo = models.PositiveIntegerField(default=0, )
    notas_insumo = models.TextField(max_length=500, blank=True)
    
    
    def __str__(self) -> str:
        return self.nombre +" "+str(self.codigo_insumo) 

# class MovimientoInsumos(models.Model):
#      quien_saca = models.ForeignKey()
class PrestamoInsumos(models.Model):
    MOVIMIENTO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('prestamo', 'Préstamo'),
        ('devolucion', 'Devolución')
    ]
    TIPO_MEDIDAS_CHOICES = [
        ('g', 'Gramos'),
        ('m', 'Metros'),
        ('und', 'Unidades'),
        ('L', 'Litros')
    ]

    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=20, choices=MOVIMIENTO_CHOICES)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    unidad_medida = models.CharField(choices=TIPO_MEDIDAS_CHOICES, max_length=50, default=None )
    prestado_por = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='el_que_presta',null=True)
    prestado_a = models.ForeignKey(User, on_delete=models.SET_NULL,  related_name='el_que_recibe',null=True)
    devolucion_recibida = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='el_que_devuelve',null=True)
    esta_devuelto = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de insumos"
        verbose_name_plural = "Registros de insumos"

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.insumo.nombre} - {self.cantidad} - {self.fecha.strftime('%Y-%m-%d')}"