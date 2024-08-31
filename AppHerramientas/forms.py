from django import forms

class ToolsForm(forms.Form):
    name_tools = forms.CharField(max_length=50, label='Nombre de la herramienta')
    cantidad = forms.IntegerField( )