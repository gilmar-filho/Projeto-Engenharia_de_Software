"""
Implementação do DAO para Responsável usando arquivo CSV
"""

import csv
import os
from typing import List, Optional
from dao.interfaces.responsavel_dao_interface import ResponsavelDAOInterface
from models.responsavel import Responsavel


class ResponsavelDAO(ResponsavelDAOInterface):
    """
    Implementação do DAO para Responsavel usando arquivo CSV como persistência.
    """
    
    def __init__(self, arquivo_csv: str = "data/responsaveis.csv"):
        """
        Inicializa o DAO do Responsável.
        
        Args:
            arquivo_csv (str): Caminho para o arquivo CSV
        """
        self.arquivo_csv = arquivo_csv
        self._criar_arquivo_se_nao_existir()
    
    def _criar_arquivo_se_nao_existir(self) -> None:
        """Cria o arquivo CSV se ele não existir."""
        if not os.path.exists(self.arquivo_csv):
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(self.arquivo_csv), exist_ok=True)
            
            # Cria o arquivo com cabeçalho
            with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(['cpf', 'nome', 'telefone', 'setor'])
    
    def _carregar_responsaveis(self) -> List[Responsavel]:
        """
        Carrega os responsáveis do arquivo CSV.
        
        Returns:
            List[Responsavel]: Lista de responsáveis carregados
        """
        responsaveis = []
        
        try:
            with open(self.arquivo_csv, 'r', encoding='utf-8') as arquivo:
                reader = csv.DictReader(arquivo)
                for linha in reader:
                    if linha['cpf'] and linha['cpf'].strip():  # Pula linhas vazias
                        responsavel = Responsavel(
                            cpf=linha['cpf'].strip(),
                            nome=linha['nome'].strip(),
                            telefone=linha['telefone'].strip(),
                            setor=linha['setor'].strip()
                        )
                        responsaveis.append(responsavel)
        except FileNotFoundError:
            responsaveis = []
        except Exception as e:
            print(f"Erro ao carregar responsáveis: {e}")
            responsaveis = []
        
        return responsaveis
    
    def _salvar_responsaveis(self, responsaveis: List[Responsavel]) -> None:
        """
        Salva todos os responsáveis no arquivo CSV.
        
        Args:
            responsaveis (List[Responsavel]): Lista de responsáveis a serem salvos
        """
        try:
            with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(['cpf', 'nome', 'telefone', 'setor'])
                
                for responsavel in responsaveis:
                    writer.writerow([
                        responsavel.get_cpf(),
                        responsavel.get_nome(),
                        responsavel.get_telefone(),
                        responsavel.get_setor()
                    ])
        except Exception as e:
            print(f"Erro ao salvar responsáveis: {e}")
            raise
    
    def salvar(self, responsavel: Responsavel) -> None:
        """
        Salva um responsável no repositório.
        
        Args:
            responsavel (Responsavel): Responsável a ser salvo
            
        Raises:
            ValueError: Se já existe um responsável com o mesmo CPF
        """
        # Carrega responsáveis existentes
        responsaveis_existentes = self._carregar_responsaveis()
        
        # Verifica se já existe um responsável com o mesmo CPF
        for resp in responsaveis_existentes:
            if resp.get_cpf() == responsavel.get_cpf():
                raise ValueError(f"Já existe um responsável com o CPF {responsavel.get_cpf()}")
        
        # Adiciona o novo responsável e salva
        responsaveis_existentes.append(responsavel)
        self._salvar_responsaveis(responsaveis_existentes)
    
    def listar_todos(self) -> List[Responsavel]:
        """
        Lista todos os responsáveis.
        
        Returns:
            List[Responsavel]: Lista com todos os responsáveis
        """
        return self._carregar_responsaveis()
    
    def buscar_por_cpf(self, cpf: str) -> Optional[Responsavel]:
        """
        Busca um responsável pelo CPF.
        
        Args:
            cpf (str): CPF do responsável
            
        Returns:
            Optional[Responsavel]: Responsável encontrado ou None
        """
        responsaveis = self._carregar_responsaveis()
        for responsavel in responsaveis:
            if responsavel.get_cpf() == cpf:
                return responsavel
        return None
    
    def remover(self, responsavel: Responsavel) -> None:
        """
        Remove um responsável do repositório.
        
        Args:
            responsavel (Responsavel): Responsável a ser removido
        """
        responsaveis = self._carregar_responsaveis()
        responsaveis_filtrados = [r for r in responsaveis if r.get_cpf() != responsavel.get_cpf()]
        self._salvar_responsaveis(responsaveis_filtrados)
    
    def atualizar(self, responsavel: Responsavel) -> None:
        """
        Atualiza os dados de um responsável.
        
        Args:
            responsavel (Responsavel): Responsável com dados atualizados
            
        Raises:
            ValueError: Se o responsável não for encontrado
        """
        responsaveis = self._carregar_responsaveis()
        for i, r in enumerate(responsaveis):
            if r.get_cpf() == responsavel.get_cpf():
                responsaveis[i] = responsavel
                self._salvar_responsaveis(responsaveis)
                return
        raise ValueError(f"Responsável com CPF {responsavel.get_cpf()} não encontrado")
    
    def existe_cpf(self, cpf: str) -> bool:
        """
        Verifica se existe um responsável com o CPF informado.
        
        Args:
            cpf (str): CPF a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        return self.buscar_por_cpf(cpf) is not None