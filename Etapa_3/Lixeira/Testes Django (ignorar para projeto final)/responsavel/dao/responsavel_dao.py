# responsavel/dao/responsavel_dao.py

from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from responsavel.dao.responsavel_dao_interface import ResponsavelDAOInterface
from responsavel.models import Responsavel


class ResponsavelDAO(ResponsavelDAOInterface):
    """
    Implementação concreta do DAO para Responsavel.
    Gerencia todas as operações de persistência da entidade Responsavel.
    """
    
    def salvar(self, responsavel: Responsavel) -> None:
        """
        Salva um responsável no banco de dados.
        
        Args:
            responsavel (Responsavel): O responsável a ser salvo
            
        Raises:
            IntegrityError: Se já existe um responsável com o mesmo CPF
            ValueError: Se o responsável é inválido
        """
        if not responsavel:
            raise ValueError("Responsável não pode ser None")
        
        if not isinstance(responsavel, Responsavel):
            raise ValueError("Objeto deve ser uma instância de Responsavel")
        
        try:
            with transaction.atomic():
                responsavel.save()
        except IntegrityError:
            raise IntegrityError(f"Já existe um responsável com o CPF {responsavel.cpf}")
    
    def listar_todos(self) -> List[Responsavel]:
        """
        Lista todos os responsáveis cadastrados ordenados por nome.
        
        Returns:
            List[Responsavel]: Lista com todos os responsáveis
        """
        return list(Responsavel.objects.all().order_by('nome'))
    
    def buscar_por_cpf(self, cpf: str) -> Optional[Responsavel]:
        """
        Busca um responsável pelo seu CPF.
        
        Args:
            cpf (str): CPF do responsável (apenas números)
            
        Returns:
            Optional[Responsavel]: O responsável encontrado ou None
        """
        if not cpf or not isinstance(cpf, str):
            return None
        
        try:
            return Responsavel.objects.get(cpf=cpf.strip())
        except ObjectDoesNotExist:
            return None
    
    def remover(self, responsavel: Responsavel) -> None:
        """
        Remove um responsável do banco de dados.
        
        Args:
            responsavel (Responsavel): O responsável a ser removido
            
        Raises:
            ValueError: Se o responsável é inválido
            IntegrityError: Se o responsável possui bombonas associadas
        """
        if not responsavel:
            raise ValueError("Responsável não pode ser None")
        
        if not isinstance(responsavel, Responsavel):
            raise ValueError("Objeto deve ser uma instância de Responsavel")
        
        try:
            # Verifica se existem bombonas associadas
            if responsavel.bombonas.exists():
                raise IntegrityError(
                    f"Não é possível remover o responsável {responsavel.nome}. "
                    f"Existem {responsavel.bombonas.count()} bombona(s) associada(s)."
                )
            
            with transaction.atomic():
                responsavel.delete()
        except IntegrityError:
            raise  # Re-propaga a exceção de integridade
    
    def atualizar(self, responsavel: Responsavel) -> None:
        """
        Atualiza os dados de um responsável existente.
        
        Args:
            responsavel (Responsavel): O responsável com os dados atualizados
            
        Raises:
            ValueError: Se o responsável é inválido
            ObjectDoesNotExist: Se o responsável não existe no banco
        """
        if not responsavel:
            raise ValueError("Responsável não pode ser None")
        
        if not isinstance(responsavel, Responsavel):
            raise ValueError("Objeto deve ser uma instância de Responsavel")
        
        if not self.existe_cpf(responsavel.cpf):
            raise ObjectDoesNotExist(f"Responsável com CPF {responsavel.cpf} não encontrado")
        
        try:
            with transaction.atomic():
                responsavel.save()
        except IntegrityError as e:
            raise IntegrityError(f"Erro ao atualizar responsável: {str(e)}")
    
    def existe_cpf(self, cpf: str) -> bool:
        """
        Verifica se já existe um responsável com o CPF informado.
        
        Args:
            cpf (str): CPF a ser verificado
            
        Returns:
            bool: True se o CPF já existe, False caso contrário
        """
        if not cpf or not isinstance(cpf, str):
            return False
        
        return Responsavel.objects.filter(cpf=cpf.strip()).exists()
    
    def buscar_por_nome(self, nome: str) -> List[Responsavel]:
        """
        Busca responsáveis por nome (busca parcial, case-insensitive).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado
            
        Returns:
            List[Responsavel]: Lista de responsáveis encontrados
        """
        if not nome or not isinstance(nome, str):
            return []
        
        return list(
            Responsavel.objects.filter(
                nome__icontains=nome.strip()
            ).order_by('nome')
        )
    
    def buscar_por_setor(self, setor: str) -> List[Responsavel]:
        """
        Busca responsáveis por setor (busca parcial, case-insensitive).
        
        Args:
            setor (str): Setor ou parte do setor a ser buscado
            
        Returns:
            List[Responsavel]: Lista de responsáveis encontrados
        """
        if not setor or not isinstance(setor, str):
            return []
        
        return list(
            Responsavel.objects.filter(
                setor__icontains=setor.strip()
            ).order_by('nome')
        )
    
    def contar_total(self) -> int:
        """
        Conta o total de responsáveis cadastrados.
        
        Returns:
            int: Número total de responsáveis
        """
        return Responsavel.objects.count()
    
    def listar_setores_unicos(self) -> List[str]:
        """
        Lista todos os setores únicos cadastrados.
        
        Returns:
            List[str]: Lista de setores únicos ordenados
        """
        setores = Responsavel.objects.values_list('setor', flat=True).distinct()
        return sorted([setor for setor in setores if setor])
    
    def responsaveis_com_bombonas(self) -> List[Responsavel]:
        """
        Lista responsáveis que possuem pelo menos uma bombona.
        
        Returns:
            List[Responsavel]: Lista de responsáveis com bombonas
        """
        return list(
            Responsavel.objects.filter(
                bombonas__isnull=False
            ).distinct().order_by('nome')
        )
    
    def responsaveis_sem_bombonas(self) -> List[Responsavel]:
        """
        Lista responsáveis que não possuem bombonas.
        
        Returns:
            List[Responsavel]: Lista de responsáveis sem bombonas
        """
        return list(
            Responsavel.objects.filter(
                bombonas__isnull=True
            ).order_by('nome')
        )