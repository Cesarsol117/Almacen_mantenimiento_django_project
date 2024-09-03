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
from AppHerramientas.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', inicio_herramientas, name='home_tools'),
    path('new_tools/', create_tools, name='form_tools'),
    path('all_tools/', view_all_tools, name='list_tools'),
    path('delete_tools/<identification>', delete_tools, name='delete_to_tools'),
    path('edit_tools/<identification>', edit_tools, name='edit_to_tools'),
]
