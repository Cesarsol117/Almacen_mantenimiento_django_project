from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Curso
from django.http import HttpResponse
from AppInsumos.forms import InsumoForm


from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin #vistas basadas en clases
from django.contrib.auth.decorators import login_required #vistas basadas en funciones

from AppUsers.models import Avatar

# Create your views here.

DEFAULT_AVATAR_PATH = '/media/Avatares/TrianguloIsoceles.jpg'

def pagina_inicio(request):
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(user=request.user).first()  # Obtén el primer avatar si existe
        if avatar:
            avatar_image = avatar.user_imagen.url  # Obtén la URL del avatar
        else:
            avatar_image = DEFAULT_AVATAR_PATH  # Usa la imagen por defecto si no tiene avatar
        return render(request, 'inicio.html', {"avatar_image_user": avatar_image})
    else:
        return render(request, 'inicio.html')

# def curso(request):
#     curso = Curso(nombre = 'Python', numero_curso = 1234)
#     curso.save()
#     cadena_texto = 'Curso guardado: ' +curso.nombre+' '+str(curso.numero_curso)
#     return   HttpResponse(cadena_texto)

def pagina_cursos(request):
    return render(request, 'cursos.html')
@login_required
def all_insumos(request):
    all_insumos = Curso.objects.all()
    return render(request, 'cursos.html', {'los_insumos':all_insumos})

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

@login_required
def busqueda_formulario(request):
    if request.GET['comision']:
        comision = request.GET['comision']
        insumos_buscado = Curso.objects.filter(numero_curso = comision )
        return render(request, 'resultadoBusqueda.html', {'insumos_buscado':insumos_buscado})
    else:
        return render(request, 'busquedaInsumos.html', {'mensaje':'Coloca un número...'})
    
# Update

class InsumoUpdate(LoginRequiredMixin, UpdateView):
    model = Curso
    success_url = reverse_lazy('todos_insumos')
    fields = ['nombre', 'numero_curso']
    
# delete
class InsumoDelete(DeleteView):
    model = Curso
    template_name = 'AppInsumos/curso_confirm_delete.html'
    success_url = reverse_lazy('todos_insumos')
    context_object_name = 'curso'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensaje'] = 'Confirmación de eliminación de curso'
        return context
