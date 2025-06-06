# bombona/dao/bombona_dao.py

from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.db.models import Sum, Count, Q
from bombona.dao.bombona_dao_interface import BombonaDAOInterface
from bombona.models import Bombona
from responsavel.models import Responsavel


class BombonaDAO(BombonaDAOInterface):
    """
    Implementação concreta do DAO para Bombona.
    Gerencia todas as operações de persistência da entidade Bombona.
    """
    
    def salvar(self, bombona: Bombona) -> None:
        """
        Salva uma bombona no banco de dados.
        
        Args:
            bombona (Bombona): A bombona a ser salva
            
        Raises:
            IntegrityError: Se já existe uma bombona com o mesmo código
            ValueError: Se a bombona é inválida
        """
        if not bombona:
            raise ValueError("Bombona não pode ser None")
        
        if not isinstance(bombona, Bombona):
            raise ValueError("Objeto deve ser uma instância de Bombona")
        
        try:
            with transaction.atomic():
                bombona.save()
        except IntegrityError:
            raise IntegrityError(f"Já existe uma bombona com o código {bombona.codigo}")
    
    def listar_todas(self) -> List[Bombona]:
        """
        Lista todas as bombonas cadastradas ordenadas por código.
        
        Returns:
            List[Bombona]: Lista com todas as bombonas
        """
        return list(
            Bombona.objects.all()
            .select_related('responsavel')  # Otimização para evitar N+1 queries
            .order_by('codigo')
        )
    
    def buscar_por_codigo(self, codigo: str) -> Optional[Bombona]:
        """
        Busca uma bombona pelo seu código.
        
        Args:
            codigo (str): Código da bombona
            
        Returns:
            Optional[Bombona]: A bombona encontrada ou None
        """
        if not codigo or not isinstance(codigo, str):
            return None
        
        try:
            return Bombona.objects.select_related('responsavel').get(
                codigo=codigo.strip().upper()
            )
        except ObjectDoesNotExist:
            return None
    
    def buscar_por_responsavel(self, cpf: str) -> List[Bombona]:
        """
        Busca todas as bombonas de um responsável específico.
        
        Args:
            cpf (str): CPF do responsável
            
        Returns:
            List[Bombona]: Lista das bombonas do responsável
        """
        if not cpf or not isinstance(cpf, str):
            return []
        
        return list(
            Bombona.objects.filter(
                responsavel__cpf=cpf.strip()
            ).select_related('responsavel').order_by('codigo')
        )
    
    def remover(self, bombona: Bombona) -> None:
        """
        Remove uma bombona do banco de dados.
        
        Args:
            bombona (Bombona): A bombona a ser removida
            
        Raises:
            ValueError: Se a bombona é inválida
        """
        if not bombona:
            raise ValueError("Bombona não pode ser None")
        
        if not isinstance(bombona, Bombona):
            raise ValueError("Objeto deve ser uma instância de Bombona")
        
        try:
            with transaction.atomic():
                bombona.delete()
        except Exception as e:
            raise IntegrityError(f"Erro ao remover bombona: {str(e)}")
    
    def atualizar(self, bombona: Bombona) -> None:
        """
        Atualiza os dados de uma bombona existente.
        
        Args:
            bombona (Bombona): A bombona com os dados atualizados
            
        Raises:
            ValueError: Se a bombona é inválida
            ObjectDoesNotExist: Se a bombona não existe no banco
        """
        if not bombona:
            raise ValueError("Bombona não pode ser None")
        
        if not isinstance(bombona, Bombona):
            raise ValueError("Objeto deve ser uma instância de Bombona")
        
        if not self.existe_codigo(bombona.codigo):
            raise ObjectDoesNotExist(f"Bombona com código {bombona.codigo} não encontrada")
        
        try:
            with transaction.atomic():
                bombona.save()
        except IntegrityError as e:
            raise IntegrityError(f"Erro ao atualizar bombona: {str(e)}")
    
    def existe_codigo(self, codigo: str) -> bool:
        """
        Verifica se já existe uma bombona com o código informado.
        
        Args:
            codigo (str): Código a ser verificado
            
        Returns:
            bool: True se o código já existe, False caso contrário
        """
        if not codigo or not isinstance(codigo, str):
            return False
        
        return Bombona.objects.filter(codigo=codigo.strip().upper()).exists()
    
    def buscar_por_tipo_residuo(self, tipo_residuo: str) -> List[Bombona]:
        """
        Busca bombonas por tipo de resíduo (busca parcial, case-insensitive).
        
        Args:
            tipo_residuo (str): Tipo de resíduo ou parte dele
            
        Returns:
            List[Bombona]: Lista de bombonas encontradas
        """
        if not tipo_residuo or not isinstance(tipo_residuo, str):
            return []
        
        return list(
            Bombona.objects.filter(
                tipo_residuo__icontains=tipo_residuo.strip()
            ).select_related('responsavel').order_by('codigo')
        )
    
    def buscar_por_volume_range(self, volume_min: float, volume_max: float) -> List[Bombona]:
        """
        Busca bombonas por faixa de volume.
        
        Args:
            volume_min (float): Volume mínimo
            volume_max (float): Volume máximo
            
        Returns:
            List[Bombona]: Lista de bombonas na faixa de volume
        """
        if volume_min is None or volume_max is None:
            return []
        
        try:
            volume_min = float(volume_min)
            volume_max = float(volume_max)
        except (ValueError, TypeError):
            return []
        
        if volume_min > volume_max:
            volume_min, volume_max = volume_max, volume_min
        
        return list(
            Bombona.objects.filter(
                volume__gte=volume_min,
                volume__lte=volume_max
            ).select_related('responsavel').order_by('volume')
        )
    
    def contar_total(self) -> int:
        """
        Conta o total de bombonas cadastradas.
        
        Returns:
            int: Número total de bombonas
        """
        return Bombona.objects.count()
    
    def calcular_volume_total(self) -> float:
        """
        Calcula o volume total de todas as bombonas.
        
        Returns:
            float: Volume total em litros
        """
        resultado = Bombona.objects.aggregate(total=Sum('volume'))
        return resultado['total'] or 0.0
    
    def listar_tipos_residuos_unicos(self) -> List[str]:
        """
        Lista todos os tipos de resíduos únicos cadastrados.
        
        Returns:
            List[str]: Lista de tipos de resíduos únicos ordenados
        """
        tipos = Bombona.objects.values_list('tipo_residuo', flat=True).distinct()
        return sorted([tipo for tipo in tipos if tipo])
    
    def estatisticas_por_responsavel(self) -> List[dict]:
        """
        Gera estatísticas de bombonas por responsável.
        
        Returns:
            List[dict]: Lista com estatísticas por responsável
        """
        return list(
            Responsavel.objects.annotate(
                total_bombonas=Count('bombonas'),
                volume_total=Sum('bombonas__volume')
            ).filter(
                total_bombonas__gt=0
            ).values(
                'cpf', 'nome', 'setor', 'total_bombonas', 'volume_total'
            ).order_by('-total_bombonas')
        )
    
    def estatisticas_por_tipo_residuo(self) -> List[dict]:
        """
        Gera estatísticas de bombonas por tipo de resíduo.
        
        Returns:
            List[dict]: Lista com estatísticas por tipo de resíduo
        """
        return list(
            Bombona.objects.values('tipo_residuo').annotate(
                total_bombonas=Count('codigo'),
                volume_total=Sum('volume')
            ).order_by('-total_bombonas')
        )
    
    def buscar_avancada(self, filtros: dict) -> List[Bombona]:
        """
        Busca avançada com múltiplos filtros.
        
        Args:
            filtros (dict): Dicionário com filtros de busca
                - codigo: str (busca parcial)
                - tipo_residuo: str (busca parcial)
                - responsavel_nome: str (busca parcial)
                - responsavel_setor: str (busca parcial)
                - volume_min: float
                - volume_max: float
        
        Returns:
            List[Bombona]: Lista de bombonas que atendem aos filtros
        """
        queryset = Bombona.objects.select_related('responsavel')
        
        if filtros.get('codigo'):
            queryset = queryset.filter(codigo__icontains=filtros['codigo'])
        
        if filtros.get('tipo_residuo'):
            queryset = queryset.filter(tipo_residuo__icontains=filtros['tipo_residuo'])
        
        if filtros.get('responsavel_nome'):
            queryset = queryset.filter(responsavel__nome__icontains=filtros['responsavel_nome'])
        
        if filtros.get('responsavel_setor'):
            queryset = queryset.filter(responsavel__setor__icontains=filtros['responsavel_setor'])
        
        if filtros.get('volume_min') is not None:
            try:
                queryset = queryset.filter(volume__gte=float(filtros['volume_min']))
            except (ValueError, TypeError):
                pass
        
        if filtros.get('volume_max') is not None:
            try:
                queryset = queryset.filter(volume__lte=float(filtros['volume_max']))
            except (ValueError, TypeError):
                pass
        
        return list(queryset.order_by('codigo'))