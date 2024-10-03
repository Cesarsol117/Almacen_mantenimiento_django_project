from django import forms
from .models import Machine

class MachineForm(forms.Form):
    name = forms.CharField(max_length=200, label='Nombre Maquina')
    description = forms.CharField(max_length=300, label='Descripcion')
    photo = forms.ImageField(label='foto', required=False)
    
    def save(self):
        Machine.objects.create(
            name = self.cleaned_data['name'],
            description = self.cleaned_data['description'],
            photo = self.cleaned_data['photo'],
        )