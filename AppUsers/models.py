from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Avatar(models.Model):
    user_imagen = models.ImageField(("image"), upload_to='Avatares', height_field=None, width_field=None, max_length=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} - {self.user_imagen}'
     