from django.shortcuts import render
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