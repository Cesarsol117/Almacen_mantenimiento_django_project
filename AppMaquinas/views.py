from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DeleteView, UpdateView, DetailView

from AppMaquinas.models import Machine
from .forms import MachineForm

# Create your views here.

class MachineFormView(generic.FormView):
    template_name = 'AppMachines/add_machine.html'
    form_class = MachineForm
    success_url = reverse_lazy('add_machines')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class MachineListView(ListView):
    model = Machine
    template_name = "AppMachines/all_machines"
    context_object_name = 'machines'
class MachineUpdateView(UpdateView):
    model = Machine
    fields = ['name', 'description']
    template_name = 'AppMachines/update_machine.html'  # Template para el formulario de actualización
    success_url = reverse_lazy('all_machines')
    
class MachineDetailView(DetailView):
    model = Machine
    template_name = 'AppMachines/machine_detail.html'  # Template donde se mostrará la información de la máquina
    context_object_name = 'machine' 
    
class MachineDeleteView(DeleteView):
    model = Machine
    template_name = "AppMachines/curso_confirm_delete.html"
    success_url = reverse_lazy('all_machines')
    context_object_name = 'machine'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensaje'] = 'Confirmación de eliminación de curso'
        return context