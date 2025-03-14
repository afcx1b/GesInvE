# Generated by Django 5.1.5 on 2025-02-15 07:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('time_joined', models.TimeField(default=datetime.datetime.now)),
                ('ip_address', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('success', 'Éxito'), ('failed', 'Fallido')], default='success', max_length=15)),
            ],
            options={
                'verbose_name': 'Acceso de Usuario',
                'verbose_name_plural': 'Accesos de Usuarios',
                'ordering': ['id'],
                'permissions': (('view_access_users', 'Can view Acceso de Usuario'), ('delete_access_users', 'Can delete Acceso de Usuario')),
                'default_permissions': (),
            },
        ),
    ]
