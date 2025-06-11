from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Insumos
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


def get_avatar_user(request):
    avatar = Avatar.objects.filter(user=request.user).first()  # Obtén el primer avatar si existe
    if avatar:
        avatar_image = avatar.user_imagen.url  # Obtén la URL del avatar
    else:
        avatar_image = DEFAULT_AVATAR_PATH  # Usa la imagen por defecto si no tiene avatar
    return avatar_image


def pagina_inicio(request):
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(user=request.user).first()  # Obtén el primer avatar si existe
        return render(request, 'inicio.html', {"avatar_image_user": get_avatar_user(request)})
    else:
        return render(request, 'inicio.html')

# def curso(request):
#     curso = Curso(nombre = 'Python', numero_curso = 1234)
#     curso.save()
#     cadena_texto = 'Curso guardado: ' +curso.nombre+' '+str(curso.numero_curso)
#     return   HttpResponse(cadena_texto)

def pagina_cursos(request):
    return render(request, 'cursos.html')


# # Creacion del formulario y create
# # def curso_formulario(request):
#     if request.method=='POST':
#         full_form = InsumoForm(request.POST)
#         if full_form.is_valid():
#             data_form = full_form.cleaned_data
            
#             nuevo_curso = Curso(nombre = data_form['nombre'], numero_curso = data_form['numero_curso'])##estos datos deben ser iguales a los que se coloquen  en el forms.py
#             nuevo_curso.save()
#             return render(request, 'inicio.html', {'mensaje':'se guardo correctamente'})
#     else:
#         empty_form = InsumoForm()
#     return render(request, "cursoFormulario.html", {'vacio_form':empty_form})


# lista de instumos
@login_required
def all_insumos(request):
    all_insumos = Insumos.objects.all()
    return render(request, 'ListaInsumos.html', {'los_insumos':all_insumos})
# busqueda insumos
@login_required
def busqueda_formulario(request):
    if request.GET['codigo_insumo']:
        codigo_insumo = request.GET['codigo_insumo']
        insumos_buscado = Insumos.objects.filter(codigo_insumo__icontains = codigo_insumo )
        if insumos_buscado: 
            return render(request, 'ListaInsumos.html', {'los_insumos':insumos_buscado})
        else:
            return render(request, 'ListaInsumos.html', {'mensaje':'Insumo no encontrado'})
    else:
        return render(request, 'ListaInsumos.html', {'mensaje':'Coloca un número...'})
# crear
class InsumoCreateView(CreateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'crear_insumo.html'
    success_url = reverse_lazy('todos_insumos') 
# Update
class InsumoUpdate(LoginRequiredMixin, UpdateView):
    model = Insumos
    success_url = reverse_lazy('todos_insumos')
    fields = ['nombre', 'codigo_insumo', 'cantidad', 'unidad_medida', 'stock_minimo','notas_insumo']   
# delete
class InsumoDelete(DeleteView):
    model = Insumos
    template_name = 'AppInsumos/insumos_confirm_delete.html'
    success_url = reverse_lazy('todos_insumos')
    context_object_name = 'insumos'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensaje'] = 'Confirmación de eliminación de Insumo'
        return context
class InsumosDetailView(DetailView):
    model = Insumos
    template_name = "AppInsumos/DetalleCadaInsumo.html"
    context_object_name = 'insumos'

# prestamos
def busqueda_insumo(request):
    return render(request, "busquedaInsumos.html")