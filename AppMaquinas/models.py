from django.db import models

# Create your models here.


class Machine(models.Model):
    name = models.TextField(max_length=200, verbose_name="nombre")
    description = models.TextField(max_length=500, verbose_name="descripcion")
    photo = models.ImageField(upload_to='logos', null=True, blank=True, verbose_name='Foto')
    
    def __str__(self):
        return self.name
    