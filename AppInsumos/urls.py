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

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', pagina_inicio, name='home'),
    path('curso/', curso, name='courses'),
    path('pagina_cursos/', pagina_cursos, name='page_courses'),
    path('FormularioCursos/', curso_formulario, name='formulario_curso'),
    path('busquedaInsumos/', busqueda_insumo, name='busqueda_insumo'),
    path('resultadoBusqeda/', busqueda_formulario, name='formulario_busqueda'),
    
]
