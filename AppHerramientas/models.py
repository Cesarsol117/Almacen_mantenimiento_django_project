from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tools(models.Model):
    codigo = models.CharField(max_length=31,null=True, unique=True)
    nombre_herramienta = models.CharField(max_length = 50)
    cantidad = models.IntegerField()
    disponible = models.BooleanField(null=True)
    
    
    def __str__(self) -> str:
        return self.nombre_herramienta+" - "+str(self.cantidad) 

class PrestamoHerramienta(models.Model):
    MOVIMIENTO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('prestamo', 'Préstamo'),
        ('devolucion', 'Devolución')
    ]

    herramienta = models.ForeignKey(Tools, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=20, choices=MOVIMIENTO_CHOICES)
    cantidad = models.PositiveIntegerField()
    prestado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prestado_por')
    prestado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prestado_a')
    devolucion_recibida = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='devolucionador')
    esta_devuelto = models.BooleanField(null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Herramienta"
        verbose_name_plural = "Registros de Herramientas"

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.herramienta.nombre_herramienta} - {self.cantidad} - {self.fecha}"