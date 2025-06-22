"""
URL configuration for almacen_mantenimiento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from AppInsumos.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', pagina_inicio, name='home'),
    path('curso/', all_insumos, name='todos_insumos'),
    path('pagina_cursos/', pagina_cursos, name='page_courses'),
    # path('FormularioCursos/', curso_formulario, name='formulario_curso'),
    # prestamos
    path('PrestamoInsumos/<id>', prestamo_insumo, name='prestamo_insumo'),
    path('devolucion_Insumos/<id>', devolucion_insumos, name='devolucion_insumo'),
    path('resultadoBusqeda/', busqueda_formulario, name='formulario_busqueda'),
    path('resultadoBusqeda_insumo/', busqueda_por_insumo_prestado, name='formulario_busqueda_insumo'),
    # basadas en clases
    path('insumos/crear/', InsumoCreateView.as_view(), name='crear_insumo'),
    path('editarInsumos/editar/<int:pk>/', InsumoUpdate.as_view(), name='update_insumo'),
    path('eliminarInsumos/editar/<int:pk>/', InsumoDelete.as_view(), name='delete_insumo'),
    path('detalleInsumos/detalle/<int:pk>/', InsumosDetailView.as_view(), name='detail_insumo'),
    path('ListaInsumos/lista/', PrestamoInsumosListView.as_view(), name='lista_prestamo_devolucion_insumo'),

]
