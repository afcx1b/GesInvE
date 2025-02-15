from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EmployeeForm, UserForm
from .models import Employee, User
 
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login:login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    return redirect('login:login')

# 📌 VISTA: LISTAR EMPLEADOS
@login_required
def list_employees(request):
    employees = Employee.objects.all()
    return render(request, "users/employees_list.html", {"employees": employees})

# 📌 VISTA: CREAR EMPLEADO
@login_required
def create_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado registrado correctamente.")
            return redirect("employees_list")
    else:
        form = EmployeeForm()
    return render(request, "users/employees_form.html", {"form": form})

# 📌 VISTA: EDITAR EMPLEADO
@login_required
def update_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado actualizado correctamente.")
            return redirect("employees_list")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, "users/employees_form.html", {"form": form})

# 📌 VISTA: ELIMINAR EMPLEADO
@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    employee.delete()
    messages.success(request, "Empleado eliminado correctamente.")
    return redirect("employees_list")

# 📌 VISTA: LISTAR USUARIOS
@login_required
def list_users(request):
    users = User.objects.select_related("idEmployee").all()
    return render(request, "users/users_list.html", {"users": users})

# 📌 VISTA: CREAR USUARIO
@login_required
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.secretKey = make_password(form.cleaned_data["password"])  # 🔐 Cifrar contraseña
            user.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("list_users")
    else:
        form = UserForm()
    return render(request, "users/user_form.html", {"form": form})

# 📌 VISTA: EDITAR USUARIO
@login_required
def update_user(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            if "password" in form.cleaned_data and form.cleaned_data["password"]:
                user.secretKey = make_password(form.cleaned_data["password"])  # 🔐 Cifrar nueva contraseña
            user.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("list_users")
    else:
        form = UserForm(instance=user)
    return render(request, "users/user_form.html", {"form": form})

# 📌 VISTA: ELIMINAR USUARIO
@login_required
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("list_users")

# 📌 VALIDACIÓN AJAX EN TIEMPO REAL
@csrf_exempt
def validate_field(request):
    """ Valida email, cédula y fortaleza de contraseña en tiempo real con AJAX """
    field = request.GET.get("field")
    value = request.GET.get("value")

    response = {"valid": True, "message": ""}

    if field == "email":
        if User.objects.filter(idEmployee__email=value).exists():
            response["valid"] = False
            response["message"] = "Este correo ya está registrado."

    elif field == "dni":
        if Employee.objects.filter(dni=value).exists():
            response["valid"] = False
            response["message"] = "Esta cédula ya está registrada."

    elif field == "password":
        if len(value) < 8:
            response["valid"] = False
            response["message"] = "La contraseña debe tener al menos 8 caracteres."
        elif not re.search(r'[A-Z]', value):
            response["valid"] = False
            response["message"] = "Debe incluir al menos una mayúscula."
        elif not re.search(r'\d', value):
            response["valid"] = False
            response["message"] = "Debe incluir al menos un número."

    return JsonResponse(response)

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from apps.admin_tools.mixins import ValidatePermissionRequiredMixin
from apps.users.forms import UserForm, UserProfileForm
from apps.users.models import User

  
class UserListView(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    permission_required = 'view_user'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user_create')
        context['list_url'] = reverse_lazy('users_list')
        context['entity'] = 'Usuarios'
        return context


class UserCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users_list')
    permission_required = 'add_user'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class UserUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users_list')
    permission_required = 'change_user'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    permission_required = 'delete_user'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context


class UserChooseGroup(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('dashboard'))


class UserUpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('login:login')

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
