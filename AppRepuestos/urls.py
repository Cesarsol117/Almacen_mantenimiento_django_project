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
from AppRepuestos.views import RepuestosListView,search_for_spare_parts , delete_spare_part,create_spare_parts, update_spare_parts

urlpatterns = [ 
    # Login Log out Register
    path('list_spare_part/', RepuestosListView.as_view(), name='spare_parts_list'),
    # path('add_spare_part/', RepuestosCreateView.as_view(), name='spare_parts_add'),
    # path('update-spare-part//editar/<int:pk>', RepuestosUpdateView.as_view(), name='spare_parts_update'),
    path("add_spare_part/", create_spare_parts, name="spare_parts_add"),
    path("update_spare_part/<identy>", update_spare_parts, name="spare_parts_update"),
    path("delete_spare_part/<id_part>", delete_spare_part, name="delete_parts_update"),
    path("search_spare_part/", search_for_spare_parts, name="search_parts_update"),
]