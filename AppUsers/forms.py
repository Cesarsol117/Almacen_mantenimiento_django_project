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