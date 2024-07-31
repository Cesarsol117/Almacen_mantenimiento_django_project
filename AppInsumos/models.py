from django.db import models

# Create your models here.

class Curso(models.Model):
    nombre = models.CharField(max_length = 50)
    numero_curso = models.IntegerField()
     