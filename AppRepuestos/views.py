from django.shortcuts import render
from django.urls import reverse_lazy

from AppRepuestos.forms import RepuestoCreateForm
from .models import Repuestos
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
# Create your views here.

class RepuestosListView(ListView):
    model = Repuestos
    template_name = "AppRepuestos/list_spare_parts.html"
    context_object_name = "repuestos" 


# class RepuestosCreateView(CreateView):
#     model = Repuestos
#     success_url = reverse_lazy('spare_parts_list')
#     fields = ['name_spare_part', 'quantity', 'machines', 'code','storage_location','notes']

# class RepuestosUpdateView(UpdateView):
#     model = Repuestos
#     fields = ['name_spare_part', 'quantity', 'machines', 'code','storage_location','notes']
#     template_name = "AppRepuestos/spare_parts_update.html"
#     success_url = reverse_lazy('spare_parts_list')
    
def create_spare_parts(request):
    if request.method=='POST':
        full_form = RepuestoCreateForm(request.POST)
        if full_form.is_valid():
            data_form = full_form.cleaned_data
            print(data_form)
            
            new_spare_part = Repuestos.objects.create(
                name_spare_part=data_form['name_spare_part'],
                quantity=data_form['quantity'],       
                code=data_form['code'],
                storage_location=data_form['storage_location'],
                notes=data_form['notes'],
                available=data_form['quantity'] >= 1,  # Determinar si está disponible
            )
            
            # Asignar las máquinas después de crear el repuesto
            new_spare_part.machines.set(data_form['machines'])
            new_spare_part.save()
            all_spare_parts = Repuestos.objects.all()
            return render(request, "AppRepuestos/list_spare_parts.html", {'mensaje':'se guardo correctamente', 'repuestos':all_spare_parts})
    else:
        empty_form = RepuestoCreateForm()
    
    return render(request, "AppRepuestos/new_spare_part.html", {'vacio_form':empty_form})

def update_spare_parts(request, identy):
    edit_spare_part =  Repuestos.objects.get(id = identy)
    if request.method == 'POST':
        spare_part_form = RepuestoCreateForm(request.POST)
        if spare_part_form.is_valid():
            data_update_spoare_part = spare_part_form.cleaned_data
            print(data_update_spoare_part)    
            
            edit_spare_part.name_spare_part=data_update_spoare_part['name_spare_part']
            edit_spare_part.quantity       =data_update_spoare_part['quantity']       
            edit_spare_part.code=data_update_spoare_part['code'],
            edit_spare_part.storage_location=data_update_spoare_part['storage_location']
            edit_spare_part.notes=data_update_spoare_part['notes']
            if data_update_spoare_part['quantity'] == 0:
                edit_spare_part.available = False
            else:
                edit_spare_part.available = True
            
            edit_spare_part.machines.set(data_update_spoare_part['machines'])
            edit_spare_part.save()
            all_spare_parts = Repuestos.objects.all()
            return render(request, "AppRepuestos/list_spare_parts.html", {'mensaje':'se guardo correctamente', 'repuestos':all_spare_parts})
    else:
        spare_part_form = RepuestoCreateForm(initial =  {'name_spare_part':edit_spare_part.name_spare_part, 
                                                        'quantity':edit_spare_part.quantity, 
                                                        'machines':edit_spare_part.machines.all(), 
                                                        'code':edit_spare_part.code,
                                                        'storage_location':edit_spare_part.storage_location,
                                                        'notes':edit_spare_part.notes}
                                             )
    return render(request, "AppRepuestos/spare_parts_update.html", {'form':spare_part_form, 'spare_part':edit_spare_part})
    