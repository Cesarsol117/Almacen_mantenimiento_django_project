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
from AppUsers.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
    # Login Log out Register
    path('login/', login_request, name='log_in'),
    path('register/', user_register, name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edituser/', edit_user, name='edit_users'),

]