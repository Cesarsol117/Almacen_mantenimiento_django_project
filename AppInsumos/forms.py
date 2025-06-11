from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Insumos, PrestamoInsumos
# class InsumoForm(forms.Form):
#     codigo_insumo = forms.CharField(max_length=50, label='Código del insumo')
#     nombre_insumo = forms.CharField(max_length=50, label='Nombre del insumo')
#     cantidad = forms.IntegerField(min_value=0 )
#     unidad_medida = forms.ChoiceField(choices=Insumos.TIPO_MEDIDAS_CHOICES,
#                                       label= 'uniadad de medida',required=False)
#     notas_insumo = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}),
#                                     max_length=500,
#                                     label='Notas del insumo',
#                                     required=False)

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumos
        fields = ['codigo_insumo', 'nombre', 'cantidad', 'unidad_medida', 'notas_insumo']
        widgets = {
            'notas_insumo': forms.Textarea(attrs={'rows': 4}),
        }