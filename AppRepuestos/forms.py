from django import forms

from AppMaquinas.models import Machine
from .models import Repuestos


class RepuestoCreateForm(forms.Form):
    name_spare_part = forms.CharField(max_length=50, label='Nombre Repuesto')
    quantity = forms.IntegerField(min_value=0, label='Cantidad')
    code = forms.CharField(max_length=50, label='Código de Repuesto')
    storage_location = forms.CharField(max_length=100, label='Ubicación de Almacenamiento')
    notes = forms.CharField(widget=forms.Textarea, label='Notas', required=False)
    machines = forms.ModelMultipleChoiceField(queryset=Machine.objects.all(), label='Máquinas Asociadas')
    # otros campos
    
    # class Meta:
    #     model = Repuestos
    #     fields = ['name_spare_part', 'quantity', 'machines', 'notes']
