from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView

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
    
    


    