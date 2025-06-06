# responsavel/urls.py

from django.urls import path
from . import views

app_name = 'responsavel'

urlpatterns = [
    # Listagem e busca
    path('', views.listar_responsaveis, name='listar'),
    path('listar/', views.listar_responsaveis, name='listar_responsaveis'),
    
    # CRUD básico
    path('cadastrar/', views.cadastrar_responsavel, name='cadastrar'),
    path('editar/<str:cpf>/', views.editar_responsavel, name='editar'),
    path('excluir/<str:cpf>/', views.excluir_responsavel, name='excluir'),
    path('detalhes/<str:cpf>/', views.detalhes_responsavel, name='detalhes'),
    
    # APIs e relatórios
    path('api/buscar/', views.api_responsaveis, name='api_buscar'),
    path('relatorio/', views.relatorio_responsaveis, name='relatorio'),
    path('relatorio/<str:formato>/', views.relatorio_responsaveis, name='relatorio_formato'),
]