from django import forms
from django.forms import ModelForm

from .models import Machine, MachineImage

class MachineForm(forms.Form):
    name = forms.CharField(max_length=200, label='Nombre Maquina')
    description = forms.CharField(max_length=300, label='Descripcion')
    power = forms.CharField(max_length=100, label='Potencia')
    voltage = forms.CharField(max_length=100, label='Voltaje')
    amperes = forms.CharField(max_length=100, label='Amperes')
    fabricante = forms.CharField(max_length=100, label='Fabricante')
    capacity = forms.CharField( max_length=100, label='Capacidad')
    site_room = forms.CharField( max_length=100, label='Ubicacion')
    service = forms.CharField( max_length=100, label='Servicios')   

    
    def save(self):
        Machine.objects.create(
            name = self.cleaned_data['name'],
            voltage = self.cleaned_data['voltage'],
            power = self.cleaned_data['power'],
            amperes = self.cleaned_data['amperes'],
            fabricante = self.cleaned_data['fabricante'],
            capacity = self.cleaned_data['capacity'],
            site_room = self.cleaned_data['site_room'],
            service = self.cleaned_data['service'],
            description = self.cleaned_data['description'],
            
        )

class MachineImageForm(forms.ModelForm):
    image_machine = forms.ImageField(label='Imagen Maquina')
    # class Meta:
    #     model = MachineImage
    #     fields = ['image_machine']

# class MachineForm(forms.ModelForm):
#     images = forms.FileField(label='Fotos', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
#     class Meta:
#         model = Machine
#         fields = ['name', 'description', 'power', 'voltage', 'amperes', 'fabricante', 'capacity', 'site_room', 'service']
    
#     def save(self, commit=True):
#         machine = super().save(commit=commit)
#         images = self.files.getlist('images')  # Obtiene todas las imágenes subidas
#         for image in images:
#             MachineImage.objects.create(machine=machine, machine_image=image)
#         return machine