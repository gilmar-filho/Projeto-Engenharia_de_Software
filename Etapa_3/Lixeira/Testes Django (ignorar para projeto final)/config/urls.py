"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from bombona.views import dashboard, busca_global

urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),
    
    # Página inicial - redireciona para dashboard
    path('', lambda request: redirect('dashboard'), name='home'),
    
    # Dashboard principal
    path('dashboard/', dashboard, name='dashboard'),
    
    # Busca global
    path('buscar/', busca_global, name='busca_global'),
    
    # Apps do sistema
    path('responsaveis/', include('responsavel.urls')),
    path('bombonas/', include('bombona.urls')),
    
    # URLs alternativas (para flexibilidade)
    path('responsavel/', include('responsavel.urls')),
    path('bombona/', include('bombona.urls')),
]

# Configurações para desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else '')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)