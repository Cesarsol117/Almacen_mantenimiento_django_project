from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from AppHerramientas.models import PrestamoHerramienta, Tools
from AppHerramientas.forms import ToolsForm, LoanForm, ReturnToolsForm

from django.contrib.auth.mixins import LoginRequiredMixin #vistas basadas en clases
from django.contrib.auth.decorators import login_required #vistas basadas en funciones
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

# Create your views here.
@login_required
def inicio_herramientas(request):
    return render(request, "InicioHerramientas.html", {'mensaje': request.user})

def create_tools(request):
    if request.method=='POST':
        full_form = ToolsForm(request.POST)
        if full_form.is_valid():
            data_form = full_form.cleaned_data
            
            nuevo_curso = Tools(nombre_herramienta = 
                                data_form['name_tools'], 
                                cantidad = data_form['cantidad'], 
                                codigo= data_form['codigo'],
                                disponible=True)##estos datos deben ser iguales a los que se coloquen  en el forms.py
            nuevo_curso.save()
            return render(request, 'InicioHerramientas.html', {'mensaje':'se guardo correctamente'})
    else:
        empty_form = ToolsForm()
    
    return render(request, "saveTools.html", {'vacio_form':empty_form})
@login_required
def view_all_tools(request):
    all_tools = Tools.objects.all()
    return render(request, 'listTools.html', {'all_tools':all_tools})



# delete
def delete_tools(request, identification):
    tools_to_delete = Tools.objects.get(id = identification)
    tools_to_delete.delete()
    all_tools = Tools.objects.all()
    return render(request, 'listTools.html', {'all_tools':all_tools, "mensaje":"SE elimino correctamente"})


# update
def edit_tools(request, identification):
    tools_to_edit = Tools.objects.get(id=identification)
    
    if request.method == 'POST':
        form_edit = ToolsForm(request.POST)
        if form_edit.is_valid():
            edit_data = form_edit.cleaned_data
            
            tools_to_edit.codigo = edit_data['codigo']
            tools_to_edit.nombre_herramienta = edit_data['name_tools']
            tools_to_edit.cantidad           = edit_data['cantidad']
            tools_to_edit.save()
            all_tools = Tools.objects.all()
            return render(request, 'listTools.html', {'all_tools':all_tools, 'mensaje':'Se cambio Correctamente' })
        
    else:
        form_edit = ToolsForm(initial={
            'codigo':tools_to_edit.codigo,
            'name_tools':tools_to_edit.nombre_herramienta, 
            'cantidad':tools_to_edit.cantidad
            })
    return render(request, 'editTools.html', {'edit_form':form_edit, 'tools_to_edit':tools_to_edit})

@login_required
def prestamo_herramienta(request, id):
    tools_to_lend = Tools.objects.get(id=id)
    
    if request.method == 'POST':
        form_lend_edit = LoanForm(request.POST)
        if form_lend_edit.is_valid():
            edit_data_loan = form_lend_edit.cleaned_data
            
            
            tools_to_lend.cantidad -= edit_data_loan['cantidad_a_prestar']
            usuario_receptor = edit_data_loan['a_quien_se_presta']
            
            if tools_to_lend.cantidad == 0:
                tools_to_lend.disponible = False
            else:
                tools_to_lend.disponible = True
                
            tools_to_lend.save()
            regristro_de_prestamo = PrestamoHerramienta.objects.create(
                herramienta=tools_to_lend,
                tipo_movimiento='prestamo',
                cantidad=edit_data_loan['cantidad_a_prestar'],
                prestado_por=request.user,
                prestado_a=usuario_receptor,
                esta_devuelto = False,
                fecha = timezone.now()
                                            )
        return redirect('list_tools')
    else:
        form_lend_edit = LoanForm()
    return render(request, "lendTools.html", {'form':form_lend_edit, 'lend_tools':tools_to_lend })
# devoluciones
@login_required
def devoluciones_herramienta(request, id):
    herramienta_a_devolver = Tools.objects.get(id = id)
    
    relacion_de_devolucion  =  PrestamoHerramienta.objects.filter(herramienta = herramienta_a_devolver, tipo_movimiento = 'prestamo', esta_devuelto=False).order_by('fecha').first()
    
    if request.method == 'POST':
        form_devolucion = ReturnToolsForm(request.POST)
        if form_devolucion.is_valid():
            data_devolucion = form_devolucion.cleaned_data
            print(herramienta_a_devolver.cantidad)
            herramienta_a_devolver.cantidad +=  data_devolucion['cantidad_devolver']
            
            herramienta_a_devolver.disponible = herramienta_a_devolver.cantidad > 0
            
            herramienta_a_devolver.save()
            relacion_de_devolucion.esta_devuelto = True
            relacion_de_devolucion.devolucion_recibida = request.user
            relacion_de_devolucion.save()
            PrestamoHerramienta.objects.create(
                herramienta = herramienta_a_devolver,
                tipo_movimiento = 'devolucion',
                cantidad = data_devolucion['cantidad_devolver'],
                
                devolucion_recibida = request.user,
                esta_devuelto = True,
                fecha = timezone.now()
            )
        return redirect('list_tools')
    else:
        form_devolucion = ReturnToolsForm()
    return render(request, 'returnTools.html', {'form': form_devolucion, 'herramienta': herramienta_a_devolver, 'relacion_herramienta':relacion_de_devolucion})
# v5sta dev634c56nes
class RegistroEntradasSalidasListlView(ListView):
    model = PrestamoHerramienta
    template_name = "detallePrestamos.html"
    context_object_name = 'register'
    ordering = ["tipo_movimiento"]
class ToolsDetailView(DetailView):
    model = Tools
    template_name = 'DetailTools.html'  # Template donde se mostrará la información de la máquina
    context_object_name = 'herramientas'
    
