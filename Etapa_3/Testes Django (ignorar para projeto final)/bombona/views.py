# bombona/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import csv
from decimal import Decimal

from bombona.models import Bombona
from responsavel.models import Responsavel
from bombona.forms import (
    BombonaForm, BombonaBuscaForm, BombonaDeleteForm, 
    BombonaTransferenciaForm
)
from bombona.dao.bombona_dao import BombonaDAO
from responsavel.dao.responsavel_dao import ResponsavelDAO
from bombona.factories.bombona_factory import BombonaFactory


class BombonaController:
    """
    Controller para gerenciamento de bombonas.
    Implementa a lógica de negócio conforme o diagrama de classes.
    """
    
    def __init__(self):
        self.bombona_dao = BombonaDAO()
        self.bombona_factory = BombonaFactory()
        self.responsavel_dao = ResponsavelDAO()
    
    def cadastrar_bombona(self, codigo: str, volume: float, tipo_residuo: str, cpf: str) -> bool:
        """
        Cadastra uma nova bombona no sistema.
        
        Args:
            codigo (str): Código único da bombona
            volume (float): Volume em litros
            tipo_residuo (str): Tipo de resíduo químico
            cpf (str): CPF do responsável
            
        Returns:
            bool: True se cadastrada com sucesso, False caso contrário
        """
        try:
            # Buscar o responsável
            responsavel = self.responsavel_dao.buscar_por_cpf(cpf)
            if not responsavel:
                return False
            
            # Usar a factory para criar e validar a bombona
            bombona = self.bombona_factory.criar_bombona(codigo, volume, tipo_residuo, responsavel)
            
            # Usar o DAO para persistir
            self.bombona_dao.salvar(bombona)
            
            return True
        except (ValueError, IntegrityError) as e:
            # Log do erro seria implementado aqui
            return False
    
    def listar_bombonas(self) -> list:
        """
        Lista todas as bombonas cadastradas.
        
        Returns:
            list: Lista de todas as bombonas
        """
        return self.bombona_dao.listar_todas()
    
    def remover_bombona(self, codigo: str) -> bool:
        """
        Remove uma bombona do sistema.
        
        Args:
            codigo (str): Código da bombona a ser removida
            
        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        try:
            bombona = self.bombona_dao.buscar_por_codigo(codigo)
            if bombona:
                self.bombona_dao.remover(bombona)
                return True
            return False
        except Exception:
            return False
    
    def editar_bombona(self, codigo: str, novo_volume: float, novo_tipo_residuo: str, cpf_responsavel: str) -> bool:
        """
        Edita os dados de uma bombona existente.
        
        Args:
            codigo (str): Código da bombona
            novo_volume (float): Novo volume
            novo_tipo_residuo (str): Novo tipo de resíduo
            cpf_responsavel (str): CPF do responsável
            
        Returns:
            bool: True se editada com sucesso, False caso contrário
        """
        try:
            bombona = self.bombona_dao.buscar_por_codigo(codigo)
            responsavel = self.responsavel_dao.buscar_por_cpf(cpf_responsavel)
            
            if bombona and responsavel:
                # Validar os novos dados usando a factory
                if (self.bombona_factory._validar_volume(novo_volume) and
                    self.bombona_factory._validar_tipo_residuo(novo_tipo_residuo)):
                    
                    # Usar os setters conforme o diagrama
                    bombona.setVolume(novo_volume)
                    bombona.setTipoResiduo(novo_tipo_residuo)
                    bombona.setResponsavel(responsavel)
                    
                    # Persistir as mudanças
                    self.bombona_dao.atualizar(bombona)
                    return True
            return False
        except (ValueError, IntegrityError):
            return False
    
    def buscar_bombonas_por_cpf_responsavel(self, cpf: str) -> list:
        """
        Busca bombonas por CPF do responsável.
        
        Args:
            cpf (str): CPF do responsável
            
        Returns:
            list: Lista de bombonas do responsável
        """
        return self.bombona_dao.buscar_por_responsavel(cpf)
    
    def gerar_relatorio(self) -> dict:
        """
        Gera relatório completo das bombonas.
        
        Returns:
            dict: Dados do relatório
        """
        bombonas = self.listar_bombonas()
        return {
            'total_bombonas': len(bombonas),
            'volume_total': sum(b.volume for b in bombonas),
            'tipos_residuos': list(set(b.tipo_residuo for b in bombonas)),
            'estatisticas_por_responsavel': self.bombona_dao.estatisticas_por_responsavel(),
            'estatisticas_por_tipo': self.bombona_dao.estatisticas_por_tipo_residuo(),
        }


# Instância global do controller
bombona_controller = BombonaController()


def listar_bombonas(request):
    """
    View para listagem de bombonas com paginação e busca.
    """
    busca_form = BombonaBuscaForm(request.GET or None)
    bombonas = []
    
    if busca_form.is_valid():
        tipo_busca = busca_form.cleaned_data.get('tipo_busca')
        termo_busca = busca_form.cleaned_data.get('termo_busca')
        volume_min = busca_form.cleaned_data.get('volume_min')
        volume_max = busca_form.cleaned_data.get('volume_max')
        
        if tipo_busca == 'todos':
            bombonas = bombona_controller.listar_bombonas()
        elif tipo_busca == 'codigo' and termo_busca:
            bombona = bombona_controller.bombona_dao.buscar_por_codigo(termo_busca)
            bombonas = [bombona] if bombona else []
        elif tipo_busca == 'tipo_residuo' and termo_busca:
            bombonas = bombona_controller.bombona_dao.buscar_por_tipo_residuo(termo_busca)
        elif tipo_busca == 'responsavel_nome' and termo_busca:
            # Busca primeiro os responsáveis, depois suas bombonas
            responsaveis = bombona_controller.responsavel_dao.buscar_por_nome(termo_busca)
            bombonas = []
            for resp in responsaveis:
                bombonas.extend(bombona_controller.buscar_bombonas_por_cpf_responsavel(resp.cpf))
        elif tipo_busca == 'responsavel_cpf' and termo_busca:
            bombonas = bombona_controller.buscar_bombonas_por_cpf_responsavel(termo_busca)
        elif tipo_busca == 'volume_range' and volume_min is not None and volume_max is not None:
            bombonas = bombona_controller.bombona_dao.buscar_por_volume_range(volume_min, volume_max)
        elif tipo_busca == 'avancada':
            # Busca avançada com múltiplos filtros
            filtros = {}
            if termo_busca:
                filtros['tipo_residuo'] = termo_busca
            if volume_min is not None:
                filtros['volume_min'] = volume_min
            if volume_max is not None:
                filtros['volume_max'] = volume_max
            bombonas = bombona_controller.bombona_dao.buscar_avancada(filtros)
    else:
        # Se não há busca válida, lista todas
        bombonas = bombona_controller.listar_bombonas()
    
    # Paginação
    paginator = Paginator(bombonas, 12)  # 12 bombonas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas para o dashboard
    relatorio = bombona_controller.gerar_relatorio()
    
    context = {
        'bombonas': page_obj,
        'busca_form': busca_form,
        'total_bombonas': relatorio['total_bombonas'],
        'volume_total': relatorio['volume_total'],
        'total_tipos': len(relatorio['tipos_residuos']),
        'tipos_residuos': relatorio['tipos_residuos'][:5],  # Top 5 para o sidebar
    }
    
    return render(request, 'bombona/listagem_bombonas.html', context)


def cadastrar_bombona(request):
    """
    View para cadastro de nova bombona.
    """
    if request.method == 'POST':
        form = BombonaForm(request.POST)
        if form.is_valid():
            try:
                # O form já usa a factory internamente
                bombona = form.save()
                messages.success(
                    request, 
                    f'Bombona {bombona.codigo} cadastrada com sucesso!'
                )
                return redirect('bombona:listar')
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao cadastrar bombona: {str(e)}'
                )
    else:
        form = BombonaForm()
    
    # Dados para autocompletar tipos de resíduos
    tipos_existentes = bombona_controller.bombona_dao.listar_tipos_residuos_unicos()
    
    context = {
        'form': form,
        'tipos_existentes': tipos_existentes,
        'action': 'Cadastrar'
    }
    
    return render(request, 'bombona/cadastro_bombona.html', context)


def editar_bombona(request, codigo):
    """
    View para edição de bombona existente.
    """
    bombona = get_object_or_404(Bombona, codigo=codigo)
    
    if request.method == 'POST':
        form = BombonaForm(request.POST, instance=bombona)
        if form.is_valid():
            try:
                bombona_atualizada = form.save()
                messages.success(
                    request, 
                    f'Bombona {bombona_atualizada.codigo} atualizada com sucesso!'
                )
                return redirect('bombona:listar')
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao atualizar bombona: {str(e)}'
                )
    else:
        form = BombonaForm(instance=bombona)
    
    # Dados para autocompletar tipos de resíduos
    tipos_existentes = bombona_controller.bombona_dao.listar_tipos_residuos_unicos()
    
    context = {
        'form': form,
        'bombona': bombona,
        'tipos_existentes': tipos_existentes,
        'action': 'Editar'
    }
    
    return render(request, 'bombona/cadastro_bombona.html', context)


def excluir_bombona(request, codigo):
    """
    View para exclusão de bombona.
    """
    bombona = get_object_or_404(Bombona, codigo=codigo)
    
    if request.method == 'POST':
        delete_form = BombonaDeleteForm(request.POST)
        if delete_form.is_valid():
            try:
                codigo_backup = bombona.codigo
                bombona_controller.bombona_dao.remover(bombona)
                messages.success(
                    request, 
                    f'Bombona {codigo_backup} excluída com sucesso!'
                )
                return redirect('bombona:listar')
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao excluir bombona: {str(e)}'
                )
    else:
        delete_form = BombonaDeleteForm(initial={'codigo': codigo})
    
    context = {
        'bombona': bombona,
        'delete_form': delete_form,
    }
    
    return render(request, 'bombona/excluir_bombona.html', context)


def detalhes_bombona(request, codigo):
    """
    View para exibir detalhes completos de uma bombona.
    """
    bombona = get_object_or_404(Bombona, codigo=codigo)
    
    # Outras bombonas do mesmo responsável
    outras_bombonas = bombona_controller.buscar_bombonas_por_cpf_responsavel(
        bombona.responsavel.cpf
    )
    outras_bombonas = [b for b in outras_bombonas if b.codigo != codigo]
    
    # Bombonas do mesmo tipo de resíduo
    bombonas_mesmo_tipo = bombona_controller.bombona_dao.buscar_por_tipo_residuo(
        bombona.tipo_residuo
    )
    bombonas_mesmo_tipo = [b for b in bombonas_mesmo_tipo if b.codigo != codigo][:5]
    
    context = {
        'bombona': bombona,
        'outras_bombonas': outras_bombonas,
        'bombonas_mesmo_tipo': bombonas_mesmo_tipo,
    }
    
    return render(request, 'bombona/detalhes_bombona.html', context)


def transferir_bombona(request, codigo):
    """
    View para transferência de responsabilidade de bombona.
    """
    bombona = get_object_or_404(Bombona, codigo=codigo)
    
    if request.method == 'POST':
        form = BombonaTransferenciaForm(request.POST)
        if form.is_valid():
            try:
                novo_responsavel = form.cleaned_data['novo_responsavel']
                motivo = form.cleaned_data.get('motivo_transferencia', '')
                
                # Realizar a transferência
                responsavel_anterior = bombona.responsavel
                bombona.setResponsavel(novo_responsavel)
                bombona_controller.bombona_dao.atualizar(bombona)
                
                messages.success(
                    request, 
                    f'Bombona {bombona.codigo} transferida de {responsavel_anterior.nome} '
                    f'para {novo_responsavel.nome} com sucesso!'
                )
                return redirect('bombona:detalhes', codigo=codigo)
            except Exception as e:
                messages.error(
                    request, 
                    f'Erro ao transferir bombona: {str(e)}'
                )
    else:
        form = BombonaTransferenciaForm(initial={
            'bombona_codigo': bombona.codigo,
            'responsavel_atual': f"{bombona.responsavel.nome} - {bombona.responsavel.cpf}"
        })
    
    context = {
        'bombona': bombona,
        'form': form,
    }
    
    return render(request, 'bombona/transferir_bombona.html', context)


@require_http_methods(["GET"])
def api_bombonas(request):
    """
    API JSON para busca de bombonas (para uso em AJAX).
    """
    termo = request.GET.get('q', '').strip()
    
    if len(termo) < 2:
        return JsonResponse({'bombonas': []})
    
    # Busca por código ou tipo de resíduo
    bombonas_codigo = []
    bombonas_tipo = []
    
    # Busca por código
    if termo.upper().replace(' ', ''):
        bombona = bombona_controller.bombona_dao.buscar_por_codigo(termo)
        if bombona:
            bombonas_codigo = [bombona]
    
    # Busca por tipo de resíduo
    bombonas_tipo = bombona_controller.bombona_dao.buscar_por_tipo_residuo(termo)
    
    # Combina resultados sem duplicatas
    bombonas = bombonas_codigo + [b for b in bombonas_tipo if b not in bombonas_codigo]
    
    # Limita a 10 resultados
    bombonas = bombonas[:10]
    
    data = {
        'bombonas': [
            {
                'codigo': b.codigo,
                'volume': float(b.volume),
                'tipo_residuo': b.tipo_residuo,
                'responsavel_nome': b.responsavel.nome,
                'responsavel_cpf': b.responsavel.cpf,
                'display_name': f"{b.codigo} - {b.tipo_residuo} ({b.volume}L)"
            }
            for b in bombonas
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def relatorio_bombonas(request):
    """
    Gera relatório de bombonas em diferentes formatos.
    """
    formato = request.GET.get('formato', 'html')
    
    # Gerar dados do relatório usando o controller
    relatorio_data = bombona_controller.gerar_relatorio()
    bombonas = bombona_controller.listar_bombonas()
    
    context = {
        'bombonas': bombonas,
        'relatorio': relatorio_data,
    }
    
    if formato == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bombonas.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Código', 'Volume (L)', 'Tipo de Resíduo', 
            'Responsável', 'CPF Responsável', 'Setor'
        ])
        
        for bombona in bombonas:
            writer.writerow([
                bombona.codigo, bombona.volume, bombona.tipo_residuo,
                bombona.responsavel.nome, bombona.responsavel.cpf, 
                bombona.responsavel.setor
            ])
        
        return response
    
    # HTML por padrão
    return render(request, 'bombona/relatorio_bombonas.html', context)


def dashboard(request):
    """
    View principal do dashboard com estatísticas gerais.
    """
    # Dados de bombonas
    relatorio_bombonas = bombona_controller.gerar_relatorio()
    
    # Dados de responsáveis
    total_responsaveis = bombona_controller.responsavel_dao.contar_total()
    responsaveis_com_bombonas = len(
        bombona_controller.responsavel_dao.responsaveis_com_bombonas()
    )
    
    # Estatísticas por setor
    setores_stats = []
    setores = bombona_controller.responsavel_dao.listar_setores_unicos()
    for setor in setores:
        responsaveis_setor = bombona_controller.responsavel_dao.buscar_por_setor(setor)
        bombonas_setor = []
        for resp in responsaveis_setor:
            bombonas_setor.extend(
                bombona_controller.buscar_bombonas_por_cpf_responsavel(resp.cpf)
            )
        
        setores_stats.append({
            'setor': setor,
            'responsaveis': len(responsaveis_setor),
            'bombonas': len(bombonas_setor),
            'volume_total': sum(b.volume for b in bombonas_setor)
        })
    
    # Ordenar setores por volume total
    setores_stats.sort(key=lambda x: x['volume_total'], reverse=True)
    
    # Top 5 responsáveis com mais bombonas
    top_responsaveis = relatorio_bombonas['estatisticas_por_responsavel'][:5]
    
    # Top 5 tipos de resíduos mais comuns
    top_tipos = relatorio_bombonas['estatisticas_por_tipo'][:5]
    
    # Distribuição de volumes (para gráfico)
    bombonas = bombona_controller.listar_bombonas()
    volumes_distribuicao = {
        'ate_10L': len([b for b in bombonas if b.volume <= 10]),
        '10_50L': len([b for b in bombonas if 10 < b.volume <= 50]),
        '50_100L': len([b for b in bombonas if 50 < b.volume <= 100]),
        'acima_100L': len([b for b in bombonas if b.volume > 100]),
    }
    
    context = {
        'total_bombonas': relatorio_bombonas['total_bombonas'],
        'volume_total': relatorio_bombonas['volume_total'],
        'total_tipos_residuos': len(relatorio_bombonas['tipos_residuos']),
        'total_responsaveis': total_responsaveis,
        'responsaveis_com_bombonas': responsaveis_com_bombonas,
        'total_setores': len(setores),
        'setores_stats': setores_stats[:5],  # Top 5 setores
        'top_responsaveis': top_responsaveis,
        'top_tipos': top_tipos,
        'volumes_distribuicao': volumes_distribuicao,
    }
    
    return render(request, 'interface/dashboard.html', context)


@require_http_methods(["GET"])
def estatisticas_ajax(request):
    """
    Endpoint AJAX para dados de estatísticas dinâmicas.
    """
    tipo = request.GET.get('tipo', 'geral')
    
    if tipo == 'responsaveis':
        stats = bombona_controller.bombona_dao.estatisticas_por_responsavel()
        data = {
            'labels': [s['nome'] for s in stats[:10]],
            'volumes': [float(s['volume_total'] or 0) for s in stats[:10]],
            'quantidades': [s['total_bombonas'] for s in stats[:10]]
        }
    
    elif tipo == 'tipos_residuos':
        stats = bombona_controller.bombona_dao.estatisticas_por_tipo_residuo()
        data = {
            'labels': [s['tipo_residuo'] for s in stats[:10]],
            'volumes': [float(s['volume_total'] or 0) for s in stats[:10]],
            'quantidades': [s['total_bombonas'] for s in stats[:10]]
        }
    
    elif tipo == 'setores':
        setores = bombona_controller.responsavel_dao.listar_setores_unicos()
        setores_data = []
        
        for setor in setores:
            responsaveis_setor = bombona_controller.responsavel_dao.buscar_por_setor(setor)
            bombonas_setor = []
            for resp in responsaveis_setor:
                bombonas_setor.extend(
                    bombona_controller.buscar_bombonas_por_cpf_responsavel(resp.cpf)
                )
            
            setores_data.append({
                'setor': setor,
                'volume_total': sum(b.volume for b in bombonas_setor),
                'total_bombonas': len(bombonas_setor)
            })
        
        setores_data.sort(key=lambda x: x['volume_total'], reverse=True)
        
        data = {
            'labels': [s['setor'] for s in setores_data[:10]],
            'volumes': [float(s['volume_total']) for s in setores_data[:10]],
            'quantidades': [s['total_bombonas'] for s in setores_data[:10]]
        }
    
    else:  # geral
        relatorio = bombona_controller.gerar_relatorio()
        bombonas = bombona_controller.listar_bombonas()
        
        # Distribuição por faixas de volume
        distribuicao = {
            'Até 10L': len([b for b in bombonas if b.volume <= 10]),
            '10-50L': len([b for b in bombonas if 10 < b.volume <= 50]),
            '50-100L': len([b for b in bombonas if 50 < b.volume <= 100]),
            'Acima 100L': len([b for b in bombonas if b.volume > 100]),
        }
        
        data = {
            'labels': list(distribuicao.keys()),
            'quantidades': list(distribuicao.values()),
            'total_bombonas': relatorio['total_bombonas'],
            'volume_total': float(relatorio['volume_total']),
        }
    
    return JsonResponse(data)


def busca_global(request):
    """
    View para busca global no sistema (bombonas + responsáveis).
    """
    termo = request.GET.get('q', '').strip()
    resultados = {
        'bombonas': [],
        'responsaveis': [],
        'termo': termo
    }
    
    if termo and len(termo) >= 2:
        # Buscar bombonas
        bombonas_codigo = []
        if termo.replace(' ', '').isalnum():  # Pode ser um código
            bombona = bombona_controller.bombona_dao.buscar_por_codigo(termo)
            if bombona:
                bombonas_codigo = [bombona]
        
        bombonas_tipo = bombona_controller.bombona_dao.buscar_por_tipo_residuo(termo)
        resultados['bombonas'] = bombonas_codigo + [
            b for b in bombonas_tipo if b not in bombonas_codigo
        ][:10]
        
        # Buscar responsáveis
        responsaveis_nome = bombona_controller.responsavel_dao.buscar_por_nome(termo)
        responsaveis_setor = bombona_controller.responsavel_dao.buscar_por_setor(termo)
        
        # Se parece ser CPF, busca por CPF também
        if termo.replace('.', '').replace('-', '').isdigit():
            responsavel_cpf = bombona_controller.responsavel_dao.buscar_por_cpf(termo)
            if responsavel_cpf:
                responsaveis_nome.insert(0, responsavel_cpf)
        
        resultados['responsaveis'] = list(set(responsaveis_nome + responsaveis_setor))[:10]
    
    return render(request, 'interface/busca_global.html', resultados)