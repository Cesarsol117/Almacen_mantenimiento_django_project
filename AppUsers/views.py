from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin #vistas basadas en clases
from django.contrib.auth.decorators import login_required #vistas basadas en funciones
from AppInsumos.views import get_avatar_user
from AppUsers.forms import AvatarForm, UserEditForm, UserFormNew
from AppUsers.models import Avatar

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

@login_required    
def edit_user(request):
    user_to_edit = request.user
    if request.method == 'POST':
        form_to_edit = UserEditForm(request.POST)
        if form_to_edit.is_valid():
            edit_form_data = form_to_edit.cleaned_data
            user_to_edit.email = edit_form_data['email']
            user_to_edit.password1 = edit_form_data['password1']
            user_to_edit.password2 = edit_form_data['password2']
            user_to_edit.first_name = edit_form_data['first_name']
            user_to_edit.last_name = edit_form_data['last_name']
            user_to_edit.save()
            return render(request, 'inicio.html', {'mensaje':'usuario editado correctamente'})
        else:
            return render(request, 'AppUsers/edit_user_form.html', {'mensaje':'error al editar', 'form':form_to_edit, 'user_name_log': user_to_edit.username})
    else:
        form_to_edit = UserEditForm(instance = user_to_edit)
        return render(request, 'AppUsers/edit_user_form.html', {'form':form_to_edit, 'user_name_log': user_to_edit.username, "avatar_image_user": get_avatar_user(request)})

def user_log_out(request):
    return render(request, 'inicio.html', {'mensaje':'salio'})

# Editar Avatar
@login_required
def edit_user_avatar(request):
    user_avatar = Avatar.objects.filter(user=request.user).first()
    if request.method == 'POST':
        avatar_form_edit = AvatarForm(request.POST, request.FILES, instance=user_avatar)
        if avatar_form_edit.is_valid():
            avatar_image = avatar_form_edit.save(commit=False)
            avatar_image.user = request.user
            avatar_image.save()
            return render(request, 'inicio.html', {'mensaje':'Avatar agregado '})
        else:
            return render(request, 'AppUsers/add_avatar.html', {'avatar_form': avatar_form_edit, 'mensaje': 'Error al subir el avatar'})           
    else:
        avatar_form_edit = AvatarForm(instance=user_avatar)
        return render(request, 'AppUsers/add_avatar.html', {'avatar_form':avatar_form_edit, 'user_name_log':request.user, "avatar_image_user": get_avatar_user(request)})
    # avatar_to_edit = request.user
    

