from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InsumoForm(forms.Form):
    nombre = forms.CharField(max_length=50, label='Nombre del curso')
    numero_curso = forms.IntegerField( )
    
#creacion del formulario de registro por uno propip
class UserFormNew(UserCreationForm):
    email = forms.EmailField(max_length= 50, required=True)
    password1 = forms.CharField(label='ingrese Contrasena', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirme Contrasena', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:'' for k in fields}