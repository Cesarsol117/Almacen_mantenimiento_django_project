from django.db import models

# Create your models here.
class Tools(models.Model):
    nombre_herramienta = models.CharField(max_length = 50)
    cantidad = models.IntegerField()
    
    
    def __str__(self) -> str:
        return self.nombre_herramienta+" - "+str(self.cantidad) 
    