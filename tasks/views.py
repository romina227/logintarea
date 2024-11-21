from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        params = {'tasks': tasks}
        return render(request, 'tasks/index.html', params)
    else:
        return redirect('tasks:login')

def login_view(request):
    if request.method == 'POST':
        useremail = request.POST['email'] 
        password = request.POST['password']
        user = authenticate(request, username=useremail, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks:index')
        else:
            messages.error(request, 'Credenciales inválidas. Intenta nuevamente.')

    return render(request, 'tasks/login.html')
    

@login_required 
def create(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save() 
            return redirect('tasks:index')
    else:
        form = TaskCreationForm()

    return render(request, 'tasks/create.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        age = request.POST.get('age')

        try:
            User.objects.create_user(username=username, email=email, password=password, age=age)
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('tasks:login')
        except Exception as e:
            messages.error(request, f'Error en el registro: {e}')
            return render(request, 'tasks/register.html')

    return render(request, 'tasks/register.html')

@login_required
def account_detail(request):
    return render(request, 'tasks/account_detail.html')

def detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/detail.html', {'task': task})

@login_required
def edit_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        age = request.POST['age']
        request.user.username = username
        request.user.email = email
        request.user.age = age
        request.user.save()

        messages.success(request, 'La cuenta ha sido actualizada exitosamente.')
        return redirect('tasks:account_detail')

    return render(request, 'tasks/edit_account.html', {'user': request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'La contraseña ha sido cambiada exitosamente.')
            return redirect('tasks:account_detail')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.') #agregado
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'tasks/change_password.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('tasks:index') 
    return render(request, 'tasks/delete_account.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('tasks:login') 

@login_required
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskCreationForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada exitosamente.')
            return redirect('tasks:detail', task_id)
    else:
        form = TaskCreationForm(instance=task)

    return render(request, 'tasks/edit.html', {'task': task, 'form': form})

@login_required
def delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarea eliminada exitosamente.')
        return redirect('tasks:index')

    return render(request, 'tasks/delete.html', {'task': task})

def home(request):
    return render(request, 'tasks/home.html') 
