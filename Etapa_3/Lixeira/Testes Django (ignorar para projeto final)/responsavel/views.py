# responsavel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from responsavel.models import Responsavel
from responsavel.forms import ResponsavelForm, ResponsavelBuscaForm, ResponsavelDeleteForm
from responsavel.dao.responsavel_dao import ResponsavelDAO
from responsavel.factories.responsavel_factory import ResponsavelFactory


class ResponsavelController:
    """
    Controller para gerenciamento de responsáveis.
    Implementa a lógica de negócio conforme o diagrama de classes.
    """
    
    def __init__(self):
        self.responsavel_dao = ResponsavelDAO()
        self.responsavel_factory = ResponsavelFactory()
    
    def cadastrar_responsavel(self, cpf: str, nome: str, telefone: str, setor: str) -> bool:
        """
        Cadastra um novo responsável no sistema.
        
        Args:
            cpf (str): CPF do responsável
            nome (str): Nome completo
            telefone (str): Telefone de contato
            setor (str): Setor de trabalho
            
        Returns:
            bool: True se cadastrado com sucesso, False caso contrário
        """
        try:
            # Usar a factory para criar e validar o responsável
            responsavel = self.responsavel_factory.criar_responsavel(cpf, nome, telefone, setor)
            
            # Usar o DAO para persistir
            self.responsavel_dao.salvar(responsavel)
            
            return True
        except (ValueError, IntegrityError) as e:
            # Log do erro seria implementado aqui
            return False
    
    def listar_responsaveis(self) -> list:
        """
        Lista todos os responsáveis cadastrados.
        
        Returns:
            list: Lista de todos os responsáveis
        """
        return self.responsavel_dao.listar_todos()
    
    def remover_responsavel(self, cpf: str) -> bool:
        """
        Remove um responsável do sistema.
        
        Args:
            cpf (str): CPF do responsável a ser removido
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        try:
            responsavel = self.responsavel_dao.buscar_por_cpf(cpf)
            if responsavel:
                self.responsavel_dao.remover(responsavel)
                return True
            return False
        except IntegrityError:
            return False
    
    def editar_responsavel(self, cpf: str, novo_nome: str, novo_telefone: str, novo_setor: str) -> bool:
        """
        Edita os dados de um responsável existente.
        
        Args:
            cpf (str): CPF do responsável
            novo_nome (str): Novo nome
            novo_telefone (str): Novo telefone
            novo_setor (str): Novo setor
            
        Returns:
            bool: True se editado com sucesso, False caso contrário
        """
        try:
            responsavel = self.responsavel_dao.buscar_por_cpf(cpf)
            if responsavel:
                # Validar os novos dados usando a factory
                if (self.responsavel_factory._validar_nome(novo_nome) and
                    self.responsavel_factory._validar_e_formatar_telefone(novo_telefone) and
                    self.responsavel_factory._validar_setor(novo_setor)):
                    
                    # Usar os setters conforme o diagrama
                    responsavel.setNome(novo_nome)
                    responsavel.setTelefone(self.responsavel_factory._validar_e_formatar_telefone(novo_telefone))
                    responsavel.setSetor(novo_setor)
                    
                    # Persistir as mudanças
                    self.responsavel_dao.atualizar(responsavel)
                    return True
            return False
        except (ValueError, IntegrityError):
            return False
    
    def buscar_responsavel(self, cpf: str):
        """
        Busca um responsável pelo CPF.
        
        Args:
            cpf (str): CPF do responsável
            
        Returns:
            Responsavel: Responsável encontrado ou None
        """
        return self.responsavel_dao.buscar_por_cpf(cpf)


# Instância global do controller
responsavel_controller = ResponsavelController()


def listar_responsaveis(request):
    """
    View para listagem de responsáveis com paginação e busca.
    """
    busca_form = ResponsavelBuscaForm(request.GET or None)
    responsaveis = []
    
    if busca_form.is_valid():
        tipo_busca = busca_form.cleaned_data.get('tipo_busca')
        termo_busca = busca_form.cleaned_data.get('termo_busca')
        
        if tipo_busca == 'todos':
            responsaveis = responsavel_controller.listar_responsaveis()
        elif tipo_busca == 'cpf' and termo_busca:
            responsavel = responsavel_controller.buscar_responsavel(termo_busca)
            responsaveis = [responsavel] if responsavel else []
        elif tipo_busca == 'nome' and termo_busca:
            responsaveis = responsavel_controller.responsavel_dao.buscar_por_nome(termo_busca)
        elif tipo_busca == 'setor' and termo_busca:
            responsaveis = responsavel_controller.responsavel_dao.buscar_por_setor(termo_busca)
    else:
        # Se não há busca válida, lista todos
        responsaveis = responsavel_controller.listar_responsaveis()
    
    # Paginação
    paginator = Paginator(responsaveis, 10)  # 10 responsáveis por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas para o dashboard
    total_responsaveis = responsavel_controller.responsavel_dao.contar_total()
    responsaveis_com_bombonas = len(responsavel_controller.responsavel_dao.responsaveis_com_bombonas())
    setores_unicos = responsavel_controller.responsavel_dao.listar_setores_unicos()
    
    context = {
        'responsaveis': page_obj,
        'busca_form': busca_form,
        'total_responsaveis': total_responsaveis,
        'responsaveis_com_bombonas': responsaveis_com_bombonas,
        'total_setores': len(setores_unicos),
        'setores_unicos': setores_unicos,
    }
    
    return render(request, 'responsavel/listagem_responsaveis.html', context)


def cadastrar_responsavel(request):
    """
    View para cadastro de novo responsável.
    """
    if request.method == 'POST':
        form = ResponsavelForm(request.POST)
        if form.is_valid():
            try:
                # O form já usa a factory internamente
                responsavel = form.save()
                messages.success(
                    request, 
                    f'Responsável {responsavel.nome} cadastrado com sucesso!'
                )
                return redirect('responsavel:listar')
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao cadastrar responsável: {str(e)}'
                )
    else:
        form = ResponsavelForm()
    
    # Dados para autocompletar setores
    setores_existentes = responsavel_controller.responsavel_dao.listar_setores_unicos()
    
    context = {
        'form': form,
        'setores_existentes': setores_existentes,
        'action': 'Cadastrar'
    }
    
    return render(request, 'responsavel/cadastro_responsavel.html', context)


def editar_responsavel(request, cpf):
    """
    View para edição de responsável existente.
    """
    responsavel = get_object_or_404(Responsavel, cpf=cpf)
    
    if request.method == 'POST':
        form = ResponsavelForm(request.POST, instance=responsavel)
        if form.is_valid():
            try:
                responsavel_atualizado = form.save()
                messages.success(
                    request, 
                    f'Responsável {responsavel_atualizado.nome} atualizado com sucesso!'
                )
                return redirect('responsavel:listar')
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao atualizar responsável: {str(e)}'
                )
    else:
        form = ResponsavelForm(instance=responsavel)
    
    # Dados para autocompletar setores
    setores_existentes = responsavel_controller.responsavel_dao.listar_setores_unicos()
    
    context = {
        'form': form,
        'responsavel': responsavel,
        'setores_existentes': setores_existentes,
        'action': 'Editar'
    }
    
    return render(request, 'responsavel/cadastro_responsavel.html', context)


def excluir_responsavel(request, cpf):
    """
    View para exclusão de responsável.
    """
    responsavel = get_object_or_404(Responsavel, cpf=cpf)
    
    # Verifica se tem bombonas associadas
    total_bombonas = responsavel.bombonas.count()
    
    if request.method == 'POST':
        delete_form = ResponsavelDeleteForm(request.POST)
        if delete_form.is_valid():
            try:
                if total_bombonas > 0:
                    messages.error(
                        request, 
                        f'Não é possível excluir {responsavel.nome}. '
                        f'Existem {total_bombonas} bombona(s) associada(s).'
                    )
                else:
                    nome = responsavel.nome
                    responsavel_controller.responsavel_dao.remover(responsavel)
                    messages.success(
                        request, 
                        f'Responsável {nome} excluído com sucesso!'
                    )
                    return redirect('responsavel:listar')
            except IntegrityError as e:
                messages.error(
                    request, 
                    f'Erro ao excluir responsável: {str(e)}'
                )
    else:
        delete_form = ResponsavelDeleteForm(initial={'cpf': cpf})
    
    context = {
        'responsavel': responsavel,
        'delete_form': delete_form,
        'total_bombonas': total_bombonas,
    }
    
    return render(request, 'responsavel/excluir_responsavel.html', context)


def detalhes_responsavel(request, cpf):
    """
    View para exibir detalhes completos de um responsável.
    """
    responsavel = get_object_or_404(Responsavel, cpf=cpf)
    
    # Buscar bombonas do responsável
    bombonas = responsavel_controller.responsavel_dao.responsavel_dao.buscar_por_responsavel(cpf)
    
    # Estatísticas
    total_bombonas = len(bombonas)
    volume_total = sum(bombona.volume for bombona in bombonas) if bombonas else 0
    tipos_residuos = list(set(bombona.tipo_residuo for bombona in bombonas))
    
    context = {
        'responsavel': responsavel,
        'bombonas': bombonas,
        'total_bombonas': total_bombonas,
        'volume_total': volume_total,
        'tipos_residuos': tipos_residuos,
    }
    
    return render(request, 'responsavel/detalhes_responsavel.html', context)


@require_http_methods(["GET"])
def api_responsaveis(request):
    """
    API JSON para busca de responsáveis (para uso em AJAX).
    """
    termo = request.GET.get('q', '').strip()
    
    if len(termo) < 2:
        return JsonResponse({'responsaveis': []})
    
    # Busca por nome ou CPF
    responsaveis_nome = responsavel_controller.responsavel_dao.buscar_por_nome(termo)
    
    # Se o termo parece ser um CPF, busca também por CPF
    if termo.replace('.', '').replace('-', '').isdigit():
        responsavel_cpf = responsavel_controller.buscar_responsavel(termo)
        if responsavel_cpf and responsavel_cpf not in responsaveis_nome:
            responsaveis_nome.insert(0, responsavel_cpf)
    
    # Limita a 10 resultados
    responsaveis = responsaveis_nome[:10]
    
    data = {
        'responsaveis': [
            {
                'cpf': r.cpf,
                'nome': r.nome,
                'telefone': r.telefone,
                'setor': r.setor,
                'display_name': f"{r.nome} - {r.cpf}"
            }
            for r in responsaveis
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def relatorio_responsaveis(request):
    """
    Gera relatório de responsáveis em diferentes formatos.
    """
    formato = request.GET.get('formato', 'html')
    
    # Dados do relatório
    responsaveis = responsavel_controller.listar_responsaveis()
    responsaveis_com_bombonas = responsavel_controller.responsavel_dao.responsaveis_com_bombonas()
    responsaveis_sem_bombonas = responsavel_controller.responsavel_dao.responsaveis_sem_bombonas()
    setores_unicos = responsavel_controller.responsavel_dao.listar_setores_unicos()
    
    context = {
        'responsaveis': responsaveis,
        'total_responsaveis': len(responsaveis),
        'responsaveis_com_bombonas': len(responsaveis_com_bombonas),
        'responsaveis_sem_bombonas': len(responsaveis_sem_bombonas),
        'total_setores': len(setores_unicos),
        'setores': setores_unicos,
    }
    
    if formato == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="responsaveis.csv"'
        
        import csv
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Nome', 'Telefone', 'Setor', 'Total Bombonas'])
        
        for responsavel in responsaveis:
            total_bombonas = responsavel.bombonas.count()
            writer.writerow([
                responsavel.cpf, responsavel.nome, 
                responsavel.telefone, responsavel.setor, 
                total_bombonas
            ])
        
        return response
    
    # HTML por padrão
    return render(request, 'responsavel/relatorio_responsaveis.html', context)