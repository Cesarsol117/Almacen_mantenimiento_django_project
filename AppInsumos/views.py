from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Insumos, PrestamoInsumos
from django.http import HttpResponse
from AppInsumos.forms import DevolucionInsumoForm, InsumoForm, PrestamoInsumoForm


from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin #vistas basadas en clases
from django.contrib.auth.decorators import login_required #vistas basadas en funciones

from AppUsers.models import Avatar
from django.utils import timezone

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
        relacion_de_busqueda  = PrestamoInsumos.objects.filter(insumo__in = insumos_buscado)
        print(insumos_buscado)
        print(relacion_de_busqueda)
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
def prestamo_insumo(request, id):
    insumos_a_prestar = Insumos.objects.get(id = id)
    if request.method == 'POST':
        form_prestamo_insumo= PrestamoInsumoForm(request.POST)
        if form_prestamo_insumo.is_valid():
            data_a_editar_insumos = form_prestamo_insumo.cleaned_data
            
            insumos_a_prestar.cantidad -= data_a_editar_insumos['cantidad_a_prestar']
            unidad_medida = data_a_editar_insumos['unidades_de_prestamo']
            usuario_receptor = data_a_editar_insumos['a_quien_se_presta']
            
            insumos_a_prestar.disponible = insumos_a_prestar.cantidad > 0
            
            insumos_a_prestar.save()
            PrestamoInsumos.objects.create(
                insumo = insumos_a_prestar,
                tipo_movimiento = 'prestamo',
                cantidad = data_a_editar_insumos['cantidad_a_prestar'],
                unidad_medida = unidad_medida,
                prestado_por = request.user,
                prestado_a = usuario_receptor,
                esta_devuelto = False,
                fecha = timezone.now()
            )
        return redirect('todos_insumos')
    else:
        form_prestamo_insumo = PrestamoInsumoForm()
    return render(request, 'prestamo_herramienta.html', {'form':form_prestamo_insumo, 'insumo_a_prestar':insumos_a_prestar})            
            
    # return render(request, "busquedaInsumos.html")
    
def devolucion_insumos(request, id):
    insumo_a_devolder = Insumos.objects.get(id = id)
    relacion_de_devolcion = PrestamoInsumos.objects.filter(insumo = insumo_a_devolder, tipo_movimiento='prestamo', esta_devuelto=False).order_by('fecha').first()
    
    if request.method == 'POST':
        formulario_devolucion = DevolucionInsumoForm(request.POST)
        if formulario_devolucion.is_valid():
            data_devolucion = formulario_devolucion.cleaned_data
            print(data_devolucion)
            insumo_a_devolder.cantidad += data_devolucion['cantidad_a_devolver']
            unidad_de_medida = data_devolucion['unidades_de_devolucion']
            insumo_a_devolder.disponible = insumo_a_devolder.cantidad > 0
            insumo_a_devolder.save()
            relacion_de_devolcion.esta_devuelto = True
            relacion_de_devolcion.devolucion_recibida = request.user
            relacion_de_devolcion.save()
            PrestamoInsumos.objects.create(
                insumo = insumo_a_devolder,
                tipo_movimiento = 'devolucion',
                cantidad = data_devolucion['cantidad_a_devolver'],
                unidad_medida = unidad_de_medida,
                devolucion_recibida = request.user,
                esta_devuelto = True,
                fecha = timezone.now()
            )
        return redirect('todos_insumos')
    else:
        form_devolucion = DevolucionInsumoForm()
    return render(request, 'devolucion_insumos.html', {'form':form_devolucion, 'insumo':insumo_a_devolder, 'relacion_insumo':relacion_de_devolcion})
    
    pass

class PrestamoInsumosListView(ListView):
    model = PrestamoInsumos
    template_name = "ListaPrestamosDevoluciones.html"
    context_object_name = 'registros'
    ordering = ['tipo_movimiento']
# busqueda de insumos prestados
def busqueda_por_insumo_prestado(request):
    if request.GET['nombre_insumo']:
        nombre_insumo = request.GET['nombre_insumo']
        insumos_buscado = Insumos.objects.filter(nombre__icontains = nombre_insumo )
        relacion_de_busqeda = PrestamoInsumos.objects.filter(insumo__in = insumos_buscado)
        if relacion_de_busqeda: 
            return render(request, 'ListaPrestamosDevoluciones.html', {'registros':relacion_de_busqeda})
        else:
            return render(request, 'ListaPrestamosDevoluciones.html', {'mensaje':'Insumo no encontrado'})
    else:
        return render(request, 'ListaPrestamosDevoluciones.html', {'mensaje':'Coloca un número...'})