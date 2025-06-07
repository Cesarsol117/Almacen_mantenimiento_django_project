from django import forms
from django.contrib.auth.models import User

class ToolsForm(forms.Form):
    codigo = forms.CharField(max_length=20, label= 'codigo de herramienta')
    name_tools = forms.CharField(max_length=50, label='Nombre de la herramienta')
    cantidad = forms.IntegerField( )
    

class LoanForm(forms.Form):
    cantidad_a_prestar =  forms.IntegerField(max_value=1000, label="Cantidad a prestar")
    a_quien_se_presta =  forms.ModelChoiceField(queryset=User.objects.all(), label='Usuarios')
    
class ReturnToolsForm(forms.Form):
    cantidad_devolver = forms.IntegerField(label='Cantidad a devolver', min_value=1)
