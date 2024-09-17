from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InsumoForm(forms.Form):
    nombre = forms.CharField(max_length=50, label='Nombre del curso')
    numero_curso = forms.IntegerField( )
    
