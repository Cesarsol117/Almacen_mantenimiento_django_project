from django.shortcuts import render, get_object_or_404, redirect
from AppHerramientas.models import Tools
from AppHerramientas.forms import ToolsForm

# Create your views here.
def inicio_herramientas(request):
    return render(request, "InicioHerramientas.html")

def create_tools(request):
    if request.method=='POST':
        full_form = ToolsForm(request.POST)
        if full_form.is_valid():
            data_form = full_form.cleaned_data
            
            nuevo_curso = Tools(nombre_herramienta = data_form['name_tools'], cantidad = data_form['cantidad'])##estos datos deben ser iguales a los que se coloquen  en el forms.py
            nuevo_curso.save()
            return render(request, 'InicioHerramientas.html', {'mensaje':'se guardo correctamente'})
    else:
        empty_form = ToolsForm()
    
    return render(request, "saveTools.html", {'vacio_form':empty_form})

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
            tools_to_edit.nombre_herramienta = edit_data['name_tools']
            tools_to_edit.cantidad           = edit_data['cantidad']
            tools_to_edit.save()
            all_tools = Tools.objects.all()
            return render(request, 'listTools.html', {'all_tools':all_tools, 'mensaje':'Se cambio Correctamente' })
        
    else:
        form_edit = ToolsForm(initial={
            'name_tools':tools_to_edit.nombre_herramienta, 
            'cantidad':tools_to_edit.cantidad
            })
    return render(request, 'editTools.html', {'edit_form':form_edit, 'tools_to_edit':tools_to_edit})