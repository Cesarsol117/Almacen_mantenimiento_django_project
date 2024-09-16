from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Curso
from django.http import HttpResponse
from AppInsumos.forms import InsumoForm, UserFormNew

from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin #vistas basadas en clases
from django.contrib.auth.decorators import login_required #vistas basadas en funciones

# Create your views here.


def pagina_inicio(request):
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

# login log out y register
def login_request(request):
    if request.method == 'POST':
        form_login = AuthenticationForm(request, data= request.POST)
        if form_login.is_valid():
            user_name =form_login.cleaned_data.get('username')
            password_user =form_login.cleaned_data.get('password')
            
            login_user = authenticate(username = user_name, password = password_user ) 
            if login_user is not None:
                login(request, login_user)
                return render(request, 'inicio.html', {'mensaje':f'Bienvenido {login_user}'})
            else:
                 return render(request, 'login.html', {'mensaje':'Usuario contrasena incorrectos', 'form':form_login})
        else:
            return render(request, 'login.html', {'mensaje':'Usuario contrasena incorrectos', 'form':form_login})
            
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form':form_login})

# register
def user_register(request):
    if request.method == 'POST':
        user_new_form = UserFormNew(request.POST)
        if user_new_form.is_valid():
            username = user_new_form.cleaned_data.get('username')
            user_new_form.save()
            return render(request, 'inicio.html', {'mensaje':f'usuario {username} creado correctamente' })
        else:
            return render(request, 'new_user.html', {'form':user_new_form, 'mensaje':'error al crear el usuario'})
    else:
        user_new_form = UserFormNew()
    return render(request, 'new_user.html', {'form':user_new_form})
    
def user_log_out(request):
    return render(request, 'inicio.html', {'mensaje':'salio'})