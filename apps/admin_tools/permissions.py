from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

def assign_manage_data_permission():
    """Asigna el permiso can_manage_data a todos los superusuarios."""
    content_type = ContentType.objects.get(app_label='admin_tools', model='data_management')
    permission, _ = Permission.objects.get_or_create(
        codename='can_manage_data',
        name='Puede exportar e importar datos',
        content_type=content_type
    )

    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        user.user_permissions.add(permission)
    
    print(f"Permiso '{permission.name}' asignado a {superusers.count()} superusuarios.")

def create_admin_permissions():
    """Crea permisos personalizados para exportar/importar datos."""
    content_type, created = ContentType.objects.get_or_create(app_label='admin_tools', model='data_management')
    Permission.objects.get_or_create(codename='can_manage_data', name='Puede exportar e importar datos', content_type=content_type)
