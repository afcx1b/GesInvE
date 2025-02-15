"""
URL configuration for gesinv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from apps.homepage.views import IndexView
from apps.dashboard.views import page_not_found404
 
urlpatterns = [
    
    path('', IndexView.as_view(), name='index'),
    
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('cashier/', include('apps.cashier.urls')),
    path('categories/', include('apps.categories.urls')),
    path('products/', include('apps.products.urls')),
    path('brands/', include('apps.brands.urls')),
    path('catalogs/', include('apps.catalogs.urls')),
    path('admin_tools/', include('apps.admin_tools.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('purchases/', include('apps.purchases.urls')),
    path('expenses/', include('apps.expensess.urls')),
    
    
    path('dashboard/', include('apps.dashboard.urls')),
    path('sales/', include('apps.sales.urls')),
    path('login/', include('apps.login.urls')),
    path('reports/', include('apps.reports.urls')),
    path('security/', include('apps.security.urls')),
    
    

    path('kardex/', include('apps.kardex.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)