from django import forms

class InsumoForm(forms.Form):
    nombre = forms.CharField(max_length=50, label='Nombre del curso')
    numero_curso = forms.IntegerField( )