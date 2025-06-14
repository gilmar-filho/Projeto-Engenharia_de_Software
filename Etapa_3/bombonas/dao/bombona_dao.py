"""
Implementação do DAO para Bombona usando arquivo CSV
"""

import csv
import os
from typing import List, Optional
from dao.interfaces.bombona_dao_interface import BombonaDAOInterface
from models.bombona import Bombona


class BombonaDAO(BombonaDAOInterface):
    """
    Implementação do DAO para Bombona usando arquivo CSV como persistência.
    """
    
    def __init__(self, arquivo_csv: str = "data/bombonas.csv"):
        """ Inicializa o DAO da Bombona. """

        self.arquivo_csv = arquivo_csv
        self._criar_arquivo_se_nao_existir()
    
    def _criar_arquivo_se_nao_existir(self) -> None:
        """ Cria o arquivo CSV se ele não existir. """

        if not os.path.exists(self.arquivo_csv):
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(self.arquivo_csv), exist_ok=True)
            
            # Cria o arquivo com cabeçalho
            with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(['codigo', 'volume', 'tipo_residuo', 'cpf_responsavel'])
    
    def _carregar_bombonas(self) -> List[Bombona]:
        # Importação temporária de ResponsavelDAO para resolver a referência de CPFs no .csv
        from dao.responsavel_dao import ResponsavelDAO
        responsavel_dao = ResponsavelDAO()
        
        bombonas = []
        
        try:
            with open(self.arquivo_csv, 'r', encoding='utf-8') as arquivo:
                reader = csv.DictReader(arquivo)
                for linha in reader:
                    if linha['codigo']:
                        # Como cadastro sempre vincula responsável, 
                        # CPF sempre existirá e será válido
                        responsavel = responsavel_dao.buscar_por_cpf(linha['cpf_responsavel'])
                        
                        # Se responsável não existir, é erro de dados
                        if not responsavel:
                            print(f"ERRO: Responsável {linha['cpf_responsavel']} não encontrado para bombona {linha['codigo']}")
                            continue  # Pula esta bombona
                        
                        bombona = Bombona(
                            codigo=linha['codigo'],
                            volume=float(linha['volume']),
                            tipo_residuo=linha['tipo_residuo'],
                            responsavel=responsavel  # Sempre terá responsável
                        )
                        bombonas.append(bombona)
        except Exception as e:
            print(f"Erro ao carregar bombonas: {e}")
            return []
        
        return bombonas
    
    def _salvar_bombonas(self, bombonas: List[Bombona]) -> None:
        """ Salva todas as bombonas no arquivo CSV. """

        try:
            with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(['codigo', 'volume', 'tipo_residuo', 'cpf_responsavel'])
                
                for bombona in bombonas:
                    # Extrai o CPF do responsável
                    cpf_responsavel = ''
                    if bombona.get_responsavel():
                        cpf_responsavel = bombona.get_responsavel().get_cpf()
                    elif hasattr(bombona, '_cpf_responsavel'):
                        cpf_responsavel = bombona._cpf_responsavel
                    
                    writer.writerow([
                        bombona.get_codigo(),
                        bombona.get_volume(),
                        bombona.get_tipo_residuo(),
                        cpf_responsavel
                    ])
        except Exception as e:
            print(f"Erro ao salvar bombonas: {e}")
            raise
    
    def salvar(self, bombona: Bombona) -> None:
        """ Salva uma bombona no repositório. """

        # Carrega bombonas existentes
        bombonas_existentes = self._carregar_bombonas()
        
        # Verifica se já existe uma bombona com o mesmo código
        for bomb in bombonas_existentes:
            if bomb.get_codigo() == bombona.get_codigo():
                raise ValueError(f"Já existe uma bombona com o código {bombona.get_codigo()}")
        
        # Adiciona a nova bombona e salva
        bombonas_existentes.append(bombona)
        self._salvar_bombonas(bombonas_existentes)
    
    def listar_todas(self) -> List[Bombona]:
        """ Lista todas as bombonas. """

        return self._carregar_bombonas()
    
    def buscar_por_codigo(self, codigo: str) -> Optional[Bombona]:
        """ Busca uma bombona pelo código. """

        bombonas = self._carregar_bombonas()
        for bombona in bombonas:
            if bombona.get_codigo() == codigo:
                return bombona
        return None
    
    def buscar_por_responsavel(self, cpf: str) -> List[Bombona]:
        """ Busca bombonas por CPF do responsável. """

        bombonas = self._carregar_bombonas()
        bombonas_responsavel = []
        
        for bombona in bombonas:
            # Verifica tanto no objeto responsavel quanto no CPF armazenado
            cpf_bombona = None
            if bombona.get_responsavel():
                cpf_bombona = bombona.get_responsavel().get_cpf()
            elif hasattr(bombona, '_cpf_responsavel'):
                cpf_bombona = bombona._cpf_responsavel
            
            if cpf_bombona == cpf:
                bombonas_responsavel.append(bombona)
        
        return bombonas_responsavel
    
    def remover(self, bombona: Bombona) -> None:
        """ Remove uma bombona do repositório. """

        bombonas = self._carregar_bombonas()
        bombonas_filtradas = [b for b in bombonas if b.get_codigo() != bombona.get_codigo()]
        self._salvar_bombonas(bombonas_filtradas)
    
    def atualizar(self, bombona: Bombona) -> None:
        """ Atualiza os dados de uma bombona. """

        bombonas = self._carregar_bombonas()
        for i, b in enumerate(bombonas):
            if b.get_codigo() == bombona.get_codigo():
                bombonas[i] = bombona
                self._salvar_bombonas(bombonas)
                return
        raise ValueError(f"Bombona com código {bombona.get_codigo()} não encontrada")
    
    def existe_codigo(self, codigo: str) -> bool:
        """ Verifica se existe uma bombona com o código informado. """
        
        return self.buscar_por_codigo(codigo) is not None
