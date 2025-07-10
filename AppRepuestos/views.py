from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from AppRepuestos.forms import RepuestoCreateForm, RepuestoIngresoReturnForm, DevolucionesRepuestosForm
from .models import RegistroEntradasSalidas, Repuestos
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
#creacion
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
#actualizacion
def update_spare_parts(request, identy):
    edit_spare_part =  Repuestos.objects.get(id = identy)
    if request.method == 'POST':
        spare_part_form = RepuestoCreateForm(request.POST)
        if spare_part_form.is_valid():
            data_update_spoare_part = spare_part_form.cleaned_data
            print(data_update_spoare_part)    
            
            edit_spare_part.name_spare_part=data_update_spoare_part['name_spare_part']
            edit_spare_part.quantity       =data_update_spoare_part['quantity']       
            edit_spare_part.code=data_update_spoare_part['code']
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
# ingreso de todos los repuestos
def ingreso_spare_parts(request, id_part):
    spare_part_ingreso =  Repuestos.objects.get(id = id_part)
    if request.method == 'POST':
        spare_part_form = RepuestoIngresoReturnForm(request.POST)
        if spare_part_form.is_valid():
            data_ingreso_spare_part                 = spare_part_form.cleaned_data
            print(data_ingreso_spare_part)
            spare_part_ingreso.quantity             += data_ingreso_spare_part['quantity']
            print(spare_part_ingreso.quantity)
            spare_part_ingreso.date_to_register     = timezone.now()
            maquinas                                = data_ingreso_spare_part['machines']
            
            if data_ingreso_spare_part['quantity'] == 0:
                spare_part_ingreso.available = False
            else:
                spare_part_ingreso.available = True
            spare_part_ingreso.save()
            
            registro_de_entrada = RegistroEntradasSalidas.objects.create(
                tipo_movimiento = 'entrada',
                cantidad = data_ingreso_spare_part['quantity'],
                date_to_movent = spare_part_ingreso.date_to_register,
                spare_part_relation = spare_part_ingreso,
            )
            registro_de_entrada.machine_relation.set(maquinas)
            registro_de_entrada.save()
            
            all_spare_parts = Repuestos.objects.all()
            # return render(request, "AppRepuestos/list_spare_parts.html", {'mensaje':'se guardo correctamente', 'repuestos':all_spare_parts})
            return redirect('spare_parts_list')
   
    else:
        spare_part_form = RepuestoIngresoReturnForm(initial =  {
                                                        'quantity':'ingrese la cantidad', 
                                                        'machines':spare_part_ingreso.machines.all(), 
                                                        }
                                             )
    return render(request, "AppRepuestos/ingresos_spare_part.html", {'form':spare_part_form, 'spare_part':spare_part_ingreso})  
# salida
def out_spare_parts(request, id_part):
    out_spare_part =  Repuestos.objects.get(id = id_part)
    if request.method == 'POST':
        spare_part_form = RepuestoIngresoReturnForm(request.POST)
        if spare_part_form.is_valid():
            data_form_out_spare_part = spare_part_form.cleaned_data
            
            out_spare_part.quantity -= data_form_out_spare_part['quantity']
            out_spare_part.date_to_out       = timezone.now()
            maquinas = data_form_out_spare_part['machines']
            usuario_que_recibe = data_form_out_spare_part['a_quien_se_entrega']
            
            if out_spare_part.quantity == 0:
                out_spare_part.available = False
            else:
                out_spare_part.available = True
            
            out_spare_part.save()
            
            registro = f'Salida de {data_form_out_spare_part["quantity"]} del repuesto {out_spare_part.name_spare_part}'
            print(registro)
            
            registro_de_salida = RegistroEntradasSalidas.objects.create(
                tipo_movimiento = 'salida',
                cantidad = data_form_out_spare_part['quantity'],
                date_to_movent = out_spare_part.date_to_out,
                spare_part_relation = out_spare_part,
                entregado_a = usuario_que_recibe,
                prestado_por = request.user,
            )
            registro_de_salida.machine_relation.set(maquinas)
            registro_de_salida.save()
            
            all_spare_parts = Repuestos.objects.all()
            # return render(request, "AppRepuestos/list_spare_parts.html", {'mensaje':'se guardo correctamente', 'repuestos':all_spare_parts, 'registro':registro})
            return redirect('spare_parts_list')
    else:
        spare_part_form = RepuestoIngresoReturnForm(initial =  {
                                                            'quantity':'ingrese la cantidad', 
                                                            'machines':out_spare_part.machines.all(), 
                                                            }
                                                    )
    return render(request, "AppRepuestos/out_spare_part.html", {'form':spare_part_form, 'spare_part':out_spare_part})
# devolucion de salidas
def return_spare_part(request, id_ret):
    
    registro_salida = RegistroEntradasSalidas.objects.get(id = id_ret)
    spare_part_devolucion =  registro_salida.spare_part_relation
    
    print(f'este es el que obtiene de la salida {registro_salida}')
    print(f'repuesto de devolucion es: {spare_part_devolucion} el id es {spare_part_devolucion.id}')
    if request.method == 'POST':
        spare_part_dev_form = DevolucionesRepuestosForm(request.POST)
        if spare_part_dev_form.is_valid():
            data_dev_spare_part = spare_part_dev_form.cleaned_data
            spare_part_devolucion.quantity += data_dev_spare_part['quantity']
            if spare_part_dev_form['quantity'] == 0:
                spare_part_devolucion.available = False
            else:
                spare_part_devolucion.available = True
            spare_part_devolucion.date_to_register = timezone.now()
            maquina = data_dev_spare_part['machines']
            print(f'estoy antes del save: {spare_part_devolucion.id}')
            spare_part_devolucion.save()
            
            
            registro_de_devoluciones = RegistroEntradasSalidas.objects.create(
                tipo_movimiento = 'devoluciones',
                cantidad = data_dev_spare_part['quantity'],
                date_to_movent = spare_part_devolucion.date_to_register,
                spare_part_relation = spare_part_devolucion,
                devolucion_por = request.user,
                devuelto = True,
                se_uso = False,    
            )
            
            registro_de_devoluciones.machine_relation.set(maquina)
            registro_de_devoluciones.save()
            if registro_salida:
                registro_salida.devuelto = True
                registro_salida.se_uso = False
                registro_salida.devolucion_por = request.user
                
                registro_salida.save()
            return redirect('detail_salida_spare_parts')
    else:
        spare_part_dev_form = DevolucionesRepuestosForm(initial={
                'quantity':'ingrese la cantidad',
                'machines':spare_part_devolucion.machines.all(),
        }
            
        )    
    return render(request, "AppRepuestos/devoluciones_spare_part.html", {'form':spare_part_dev_form, 'spare_part':spare_part_devolucion, 'spare_relation':registro_salida})  
# usado
def repuesto_usado(request, id):
    
    registro_usado = RegistroEntradasSalidas.objects.get(id = id)
    print(registro_usado)
    if registro_usado:
        registro_usado.devuelto = False
        registro_usado.se_uso = True
        registro_usado.save()
        print(registro_usado.se_uso)
    return redirect('detail_salida_spare_parts')
    

# detalle de registro de repuestos
class RegistroEntradasSalidasListView(ListView):
    model = RegistroEntradasSalidas
    template_name = "AppRepuestos/detail_register_out.html"
    context_object_name = 'register'
    ordering = ["tipo_movimiento"]

class RegistroEntradasListView(ListView):
    model = RegistroEntradasSalidas
    template_name = "AppRepuestos/detail_in_spare_part.html"
    context_object_name = 'register'
    def get_queryset(self):
        return RegistroEntradasSalidas.objects.filter(tipo_movimiento = 'entrada').order_by('date_to_movent')

class RegistroSalidasListView(ListView):
    model = RegistroEntradasSalidas
    template_name = "AppRepuestos/detail_out_spare_part.html"
    context_object_name = 'register'
    def get_queryset(self):
        return RegistroEntradasSalidas.objects.filter(tipo_movimiento = 'salida').order_by('-date_to_movent')

class RegistroDevoluionesListView(ListView):
    model = RegistroEntradasSalidas
    template_name = "AppRepuestos/detail_return_spare_part.html"
    context_object_name = 'register'
    def get_queryset(self):
        return RegistroEntradasSalidas.objects.filter(tipo_movimiento = 'devoluciones').order_by('date_to_movent')

# detalle de los repuestps
class SparePartDetailView(DetailView):
    model = Repuestos
    template_name = 'AppRepuestos/detail_spare_part.html'  # Template donde se mostrará la información de la máquina
    context_object_name = 'repuestos' 

#borrado de repuestos 
def delete_spare_part(request, id_part):
    delete_part = Repuestos.objects.get(id = id_part)
    delete_part.delete()
    all_spare_parts = Repuestos.objects.all()
    return render(request, "AppRepuestos/list_spare_parts.html", {'mensaje':'se borro correctamente', 'repuestos':all_spare_parts})

def search_for_spare_parts(request):
    if request.GET['code']:
        spare_search = request.GET['code']
        find_spare_part = Repuestos.objects.filter(code__icontains = spare_search)
        return render(request, "AppRepuestos/list_spare_parts.html",{'repuestos':find_spare_part})
    else:
        return render(request, "AppRepuestos/list_spare_parts.html",{'mensaje':'din Repuestos'})