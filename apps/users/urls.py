from django.urls import path
from . import views
from apps.users.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserChooseGroup, UserUpdateProfileView, UserChangePasswordView

app_name = "users"
 
urlpatterns = [
    # 📌 URLs para empleados
    path("employees/", views.list_employees, name="employees_list"),
    path("employees/create/", views.create_employee, name="employee_create"),
    path("employees/update/<int:id>/", views.update_employee, name="employee_update"),
    path("employees/delete/<int:id>/", views.delete_employee, name="employee_delete"),

    # 📌 URLs para usuarios
    path("users/", views.list_users, name="users_list"),
    path("users/create/", views.create_user, name="user_create"),
    path("users/update/<int:id>/", views.update_user, name="user_update"),
    path("users/delete/<int:id>/", views.delete_user, name="user_delete"),

    # 📌 AJAX: Validación en tiempo real
    #path("validate-field/", views.validate_field, name="validate_field"),
    #path('login/', views.login_view, name='login'),
    #path('register/', views.register_view, name='register'),
    #path('logout/', views.logout_view, name='logout'),
    #path('profile/', views.profile_view, name='profile'),

    path('', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('choose/profile/<int:pk>/', UserChooseGroup.as_view(), name='user_choose_profile'),
    path('update/profile/', UserUpdateProfileView.as_view(), name='user_update_profile'),
    path('change/password/', UserChangePasswordView.as_view(), name='user_change_password'),
    
] 
