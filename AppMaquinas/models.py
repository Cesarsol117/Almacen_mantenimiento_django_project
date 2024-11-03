from django.db import models

# Create your models here.


class Machine(models.Model):
    name = models.CharField(max_length=200, verbose_name="nombre", null=True)
    description = models.TextField(max_length=500, verbose_name="descripcion", null=True)
    power = models.CharField(max_length=100, verbose_name='Potencia', null=True)
    voltage = models.CharField(max_length=100, verbose_name='Voltaje', null=True)
    amperes = models.CharField(max_length=100, verbose_name='Amperios', null=True)
    fabricante = models.CharField(max_length=100, verbose_name='Fabricante', null=True)
    capacity = models.CharField( max_length=100, verbose_name='Capacidad', null=True)
    site_room = models.CharField( max_length=100, verbose_name='Ubicacion', null=True)
    service = models.CharField( max_length=100, verbose_name='Servicios', null=True)

    
    def __str__(self):
        return self.name
class MachineImage(models.Model):
    machine_imagen = models.ImageField(("image"), upload_to='Maquinas', height_field=None, width_field=None, max_length=None)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='machine_photos')
    
    def __str__(self):
        return f'{self.machine} - {self.machine_imagen}' 