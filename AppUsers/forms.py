from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#creacion del formulario de registro por uno propip
class UserFormNew(UserCreationForm):
    email = forms.EmailField(max_length= 50, required=True)
    password1 = forms.CharField(label='ingrese Contrasena', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirme Contrasena', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:'' for k in fields}

class UserEditForm(UserCreationForm):
    email = forms.EmailField(max_length= 50, required=True)
    password1 = forms.CharField(label='ingrese Contrasena', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirme Contrasena', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Modificar Nombre')
    last_name = forms.CharField(label='Modificar Apellido')
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name','last_name']
        help_texts = {k:'' for k in fields}