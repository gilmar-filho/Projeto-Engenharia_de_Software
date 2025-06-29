# bombona/urls.py

from django.urls import path
from . import views

app_name = 'bombona'

urlpatterns = [
    # Listagem e busca
    path('', views.listar_bombonas, name='listar'),
    path('listar/', views.listar_bombonas, name='listar_bombonas'),
    
    # CRUD básico
    path('cadastrar/', views.cadastrar_bombona, name='cadastrar'),
    path('editar/<str:codigo>/', views.editar_bombona, name='editar'),
    path('excluir/<str:codigo>/', views.excluir_bombona, name='excluir'),
    path('detalhes/<str:codigo>/', views.detalhes_bombona, name='detalhes'),
    
    # Funcionalidades especiais
    path('transferir/<str:codigo>/', views.transferir_bombona, name='transferir'),
    
    # APIs e relatórios
    path('api/buscar/', views.api_bombonas, name='api_buscar'),
    path('api/estatisticas/', views.estatisticas_ajax, name='api_estatisticas'),
    path('relatorio/', views.relatorio_bombonas, name='relatorio'),
    path('relatorio/<str:formato>/', views.relatorio_bombonas, name='relatorio_formato'),
]