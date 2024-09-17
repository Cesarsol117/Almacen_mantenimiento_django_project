from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin #vistas basadas en clases
from django.contrib.auth.decorators import login_required #vistas basadas en funciones
from AppUsers.forms import UserFormNew

# Create your views here.



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
                 return render(request, 'AppUsers/login.html', {'mensaje':'Usuario contrasena incorrectos', 'form':form_login})
        else:
            return render(request, 'AppUsers/login.html', {'mensaje':'Usuario contrasena incorrectos', 'form':form_login})
            
    else:
        form_login = AuthenticationForm()
    return render(request, 'AppUsers/login.html', {'form':form_login})

# register
def user_register(request):
    if request.method == 'POST':
        user_new_form = UserFormNew(request.POST)
        if user_new_form.is_valid():
            username = user_new_form.cleaned_data.get('username')
            user_new_form.save()
            return render(request, 'inicio.html', {'mensaje':f'usuario {username} creado correctamente' })
        else:
            return render(request, 'AppUsers/new_user.html', {'form':user_new_form, 'mensaje':'error al crear el usuario'})
    else:
        user_new_form = UserFormNew()
    return render(request, 'AppUsers/new_user.html', {'form':user_new_form})
    
def user_log_out(request):
    return render(request, 'inicio.html', {'mensaje':'salio'})