from django.shortcuts import render
from .models import Curso
from django.http import HttpResponse
from AppInsumos.forms import InsumoForm
# Create your views here.


def pagina_inicio(request):
    return render(request, 'inicio.html')

def curso(request):
    curso = Curso(nombre = 'Python', numero_curso = 1234)
    curso.save()
    cadena_texto = 'Curso guardado: ' +curso.nombre+' '+str(curso.numero_curso)
    return   HttpResponse(cadena_texto)

def pagina_cursos(request):
    return render(request, 'cursos.html')

# Creacion del formulario y create
def curso_formulario(request):
    
    if request.method=='POST':
        full_form = InsumoForm(request.POST)
        if full_form.is_valid():
            data_form = full_form.cleaned_data
            
            nuevo_curso = Curso(nombre = data_form['nombre'], numero_curso = data_form['numero_curso'])##estos datos deben ser iguales a los que se coloquen  en el forms.py
            nuevo_curso.save()
            return render(request, 'inicio.html', {'mensaje':'se guardo correctamente'})
    else:
        empty_form = InsumoForm()
    
    return render(request, "cursoFormulario.html", {'vacio_form':empty_form})

# busqueda o ver
def busqueda_insumo(request):
    
    return render(request, "busquedaInsumos.html")
def busqueda_formulario(request):
    if request.GET['comision']:
        comision = request.GET['comision']
        insumos_buscado = Curso.objects.filter(numero_curso = comision )
        return render(request, 'resultadoBusqueda.html', {'insumos_buscado':insumos_buscado})
    else:
        return render(request, 'busquedaInsumos.html', {'mensaje':'Coloca un número...'})
# delete
