from django.shortcuts import render
from .models import Curso
from django.http import HttpResponse
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

# Creacion del formulario
def curso_formulario(request):
    if request.method=='POST':
        nuevo_curso = Curso(nombre = request.POST['curso'], numero_curso = request.POST['comision'])
        nuevo_curso.save()
        return render(request, 'inicio.html')
    return render(request, "cursoFormulario.html")