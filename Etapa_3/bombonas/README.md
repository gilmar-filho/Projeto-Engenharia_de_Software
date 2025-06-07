# Sistema de Gerenciamento de Bombonas de Resíduos Químicos

Sistema desenvolvido para a disciplina de Engenharia de Software, implementando um CRUD completo para gerenciamento de bombonas de resíduos químicos e seus responsáveis.

## 🎯 Objetivos

- Cadastrar e gerenciar responsáveis por bombonas
- Cadastrar e gerenciar bombonas de resíduos químicos
- Gerar relatórios do sistema
- Demonstrar boas práticas de Engenharia de Software

## 🏗️ Arquitetura

O sistema foi desenvolvido seguindo os padrões arquiteturais:

### **MVC (Model-View-Controller)**
- **Model**: Classes de entidade (`Bombona`, `Responsavel`)
- **View**: Interface gráfica com Tkinter
- **Controller**: Lógica de negócio (`BombonaController`, `ResponsavelController`)

### **DAO (Data Access Object)**
- Abstração do acesso aos dados
- Interfaces para baixo acoplamento
- Implementação com arquivos CSV

### **Factory Method**
- Criação controlada de objetos
- Validação centralizada
- `BombonaFactory` e `ResponsavelFactory`

## 📁 Estrutura do Projeto

```
sistema_bombonas/
│
├── main.py                          # Arquivo principal
├── requirements.txt                 # Dependências
├── README.md                       # Este arquivo
│
├── data/                           # Arquivos de dados
│   ├── bombonas.csv               # Base de dados das bombonas
│   ├── responsaveis.csv           # Base de dados dos responsáveis
│   └── __init__.py
│
├── models/                         # Entidades do sistema
│   ├── __init__.py
│   ├── bombona.py                 # Classe Bombona
│   └── responsavel.py             # Classe Responsavel
│
├── dao/                           # Acesso a dados
│   ├── __init__.py
│   ├── interfaces/                # Interfaces DAO
│   │   ├── __init__.py
│   │   ├── bombona_dao_interface.py
│   │   └── responsavel_dao_interface.py
│   ├── bombona_dao.py             # Implementação BombonaDAO
│   └── responsavel_dao.py         # Implementação ResponsavelDAO
│
├── factory/                       # Factory Methods
│   ├── __init__.py
│   ├── bombona_factory.py         # Factory para Bombona
│   └── responsavel_factory.py     # Factory para Responsavel
│
├── controllers/                   # Lógica de negócio
│   ├── __init__.py
│   ├── bombona_controller.py      # Controller de Bombona
│   └── responsavel_controller.py  # Controller de Responsavel
│
├── views/                         # Interface gráfica
│   ├── __init__.py
│   ├── tela_cadastro_bombona.py
│   ├── tela_cadastro_responsavel.py
│   ├── tela_listagem_bombonas.py
│   ├── tela_listagem_responsaveis.py
│   └── tela_relatorio.py
│
├── utils/                         # Utilitários
│   ├── __init__.py
│   └── validadores.py            # Funções de validação
│
└── tests/                        # Testes unitários
    ├── __init__.py
    └── test_models.py            # Testes das classes Model
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Tkinter (geralmente já incluído no Python)

### Instalação

1. Clone ou baixe o projeto
2. Navegue até o diretório do projeto
3. Execute o sistema:

```bash
python main.py
```

### Executar Testes

```bash
python -m unittest tests.test_models -v
```

## 💡 Funcionalidades Implementadas

### ✅ Modelos de Dados
- [x] Classe `Responsavel` com validações
- [x] Classe `Bombona` com validações
- [x] Conversão para/de dicionário
- [x] Métodos de comparação e hash

### ✅ Acesso a Dados (DAO)
- [x] Interfaces para baixo acoplamento
- [x] Implementação com CSV
- [x] CRUD completo para ambas entidades
- [x] Tratamento de erros

### ✅ Factory Methods
- [x] `ResponsavelFactory` com validações completas
- [x] `BombonaFactory` com validações completas
- [x] Validação de CPF com dígitos verificadores
- [x] Validação de telefone, nome, código, etc.

### ✅ Controllers
- [x] `ResponsavelController` com lógica de negócio
- [x] `BombonaController` com lógica de negócio
- [x] Geração de relatórios (CSV e TXT)
- [x] Estatísticas do sistema

### ✅ Interface Básica
- [x] Tela principal com estatísticas
- [x] Menu de navegação
- [x] Estrutura preparada para telas específicas

### ✅ Utilitários e Testes
- [x] Validadores auxiliares
- [x] Testes unitários básicos
- [x] Documentação completa

## 🔧 Próximas Etapas (Views)

As próximas implementações incluirão:

1. **Tela de Cadastro de Responsável**
   - Formulário com validação em tempo real
   - Máscaras para CPF e telefone
   - Seleção de setor por combobox

2. **Tela de Listagem de Responsáveis**
   - Tabela com dados formatados
   - Botões de editar e excluir
   - Busca e filtros

3. **Tela de Cadastro de Bombona**
   - Formulário com validação
   - Seleção de responsável
   - Tipos de resíduo pré-definidos

4. **Tela de Listagem de Bombonas**
   - Tabela completa com responsável
   - Filtros por tipo de resíduo e responsável
   - Operações CRUD

5. **Tela de Relatórios**
   - Geração de relatórios CSV e PDF
   - Filtros por período e categoria
   - Estatísticas visuais

## 📊 Tipos de Resíduos Válidos

- ÁCIDO
- BASE
- SOLVENTE
- METAL PESADO
- ORGÂNICO
- INORGÂNICO
- INFLAMÁVEL
- CORROSIVO
- TÓXICO
- OUTROS

## 🏢 Setores Válidos

- LABORATÓRIO
- QUÍMICA
- BIOLOGIA
- FÍSICA
- ENGENHARIA
- MEDICINA
- FARMÁCIA
- VETERINÁRIA
- AGRONOMIA
- MANUTENÇÃO
- SEGURANÇA
- ADMINISTRAÇÃO
- OUTROS

## 🔍 Validações Implementadas

### Responsável
- **CPF**: Validação com dígitos verificadores
- **Nome**: Mínimo 2 caracteres, deve ter nome e sobrenome
- **Telefone**: 10 ou 11 dígitos, DDD válido
- **Setor**: Deve estar na lista de setores válidos

### Bombona
- **Código**: 3-20 caracteres, apenas letras, números e hífens
- **Volume**: Entre 0.1 e 1000 litros
- **Tipo Resíduo**: Deve estar na lista de tipos válidos
- **Responsável**: Obrigatório e deve existir

## 🎨 Benefícios da Arquitetura

### Alta Coesão
- Cada classe tem responsabilidade única
- Módulos focados em funcionalidades específicas
- Separação clara entre camadas

### Baixo Acoplamento
- Uso de interfaces para abstrair dependências
- Controllers não dependem de implementações específicas
- Facilita testes e manutenção

### Facilidade de Manutenção
- Mudanças isoladas em camadas específicas
- Código modular e testável
- Fácil extensão de funcionalidades

### Padrões de Projeto
- **MVC**: Separação clara de responsabilidades
- **DAO**: Abstração do acesso aos dados
- **Factory Method**: Criação controlada de objetos
- **Interface Segregation**: Contratos bem definidos

## 🧪 Exemplos de Uso

### Criando um Responsável
```python
from factory.responsavel_factory import ResponsavelFactory

# Cria responsável com validação automática
responsavel = ResponsavelFactory.criar_responsavel(
    cpf="123.456.789-01",
    nome="Dr. João Silva",
    telefone="(11) 9 8765-4321",
    setor="LABORATÓRIO"
)
```

### Criando uma Bombona
```python
from factory.bombona_factory import BombonaFactory

# Cria bombona com validação automática
bombona = BombonaFactory.criar_bombona(
    codigo="LAB-001",
    volume=25.5,
    tipo_residuo="ÁCIDO",
    responsavel=responsavel
)
```

### Usando os Controllers
```python
from controllers.responsavel_controller import ResponsavelController
from controllers.bombona_controller import BombonaController

# Cadastra responsável
sucesso = responsavel_controller.cadastrar_responsavel(
    cpf="123.456.789-01",
    nome="Dr. João Silva",
    telefone="11987654321",
    setor="LABORATÓRIO"
)

# Lista todas as bombonas
bombonas = bombona_controller.listar_bombonas()

# Gera relatório
arquivo = bombona_controller.gerar_relatorio("csv")
```

## 📝 Estrutura dos Dados (CSV)

### responsaveis.csv
```csv
cpf,nome,telefone,setor
12345678901,João Silva,11987654321,LABORATÓRIO
98765432100,Maria Santos,11999888777,QUÍMICA
```

### bombonas.csv
```csv
codigo,volume,tipo_residuo,cpf_responsavel
LAB-001,25.5,ÁCIDO,12345678901
QUI-002,50.0,BASE,98765432100
```

## 🐛 Tratamento de Erros

O sistema implementa tratamento robusto de erros:

- **Validação de Entrada**: Todos os dados são validados antes da criação
- **Erros de Negócio**: Regras específicas (ex: não remover responsável com bombonas)
- **Erros de Persistência**: Tratamento de problemas com arquivos CSV
- **Mensagens Claras**: Erros informativos para o usuário

## 🔧 Configuração do Ambiente

### requirements.txt
```
# Bibliotecas padrão do Python - não necessita instalação extra
# tkinter - Interface gráfica
# csv - Manipulação de CSV
# unittest - Testes unitários
# re - Expressões regulares
# os - Operações do sistema
# sys - Configurações do sistema
```

### Estrutura de Diretórios
```bash
# Criar estrutura inicial
mkdir sistema_bombonas
cd sistema_bombonas
mkdir data models dao dao/interfaces factory controllers views utils tests

# Criar arquivos __init__.py
touch data/__init__.py
touch models/__init__.py
touch dao/__init__.py
touch dao/interfaces/__init__.py
touch factory/__init__.py
touch controllers/__init__.py
touch views/__init__.py
touch utils/__init__.py
touch tests/__init__.py
```

## 📋 Checklist de Implementação

### ✅ Fase 1 - Fundação (Concluída)
- [x] Estrutura de diretórios
- [x] Classes Model (Bombona, Responsavel)
- [x] Interfaces DAO
- [x] Implementações DAO com CSV
- [x] Factory Methods com validações
- [x] Controllers com lógica de negócio
- [x] Testes unitários básicos
- [x] Arquivo principal (main.py)
- [x] Documentação

### 🔄 Fase 2 - Interface (Próxima)
- [ ] Tela de cadastro de responsável
- [ ] Tela de listagem de responsáveis
- [ ] Tela de cadastro de bombona
- [ ] Tela de listagem de bombonas
- [ ] Tela de relatórios
- [ ] Integração completa das views

### 🔄 Fase 3 - Melhorias (Futuro)
- [ ] Validação em tempo real nas telas
- [ ] Máscaras de entrada
- [ ] Exportação para PDF
- [ ] Backup automático dos dados
- [ ] Log de operações
- [ ] Configurações do sistema

## 🎓 Conceitos de Engenharia de Software Aplicados

### Princípios SOLID
- **S**: Single Responsibility - Cada classe tem uma responsabilidade
- **O**: Open/Closed - Extensível sem modificar código existente
- **L**: Liskov Substitution - Interfaces permitem substituição
- **I**: Interface Segregation - Interfaces específicas e coesas
- **D**: Dependency Inversion - Dependências por abstração

### Padrões de Design
- **MVC**: Separação de apresentação, lógica e dados
- **DAO**: Encapsulamento do acesso aos dados
- **Factory**: Criação de objetos com validação
- **Strategy**: Diferentes implementações de DAO possíveis

### Boas Práticas
- **Documentação**: Docstrings em todas as classes/métodos
- **Tratamento de Erros**: Try/catch apropriados
- **Validação**: Dados validados antes do processamento
- **Testes**: Cobertura das funcionalidades principais
- **Nomenclatura**: Nomes descritivos e consistentes

## 🔍 Como Testar o Sistema

### Teste Manual Básico
1. Execute `python main.py`
2. Observe a tela principal com estatísticas
3. Teste os menus (ainda mostrarão mensagens de desenvolvimento)
4. Verifique a criação dos arquivos CSV em `data/`

### Teste Unitário
```bash
# Executar todos os testes
python -m unittest tests.test_models -v

# Executar teste específico
python -m unittest tests.test_models.TestResponsavel.test_criacao_responsavel -v
```

### Teste de Integração Manual
```python
# Abrir terminal Python e testar
python

# Importar e testar controllers
from controllers.responsavel_controller import ResponsavelController
from controllers.bombona_controller import BombonaController
from dao.responsavel_dao import ResponsavelDAO
from dao.bombona_dao import BombonaDAO

# Criar instâncias
resp_dao = ResponsavelDAO()
bomb_dao = BombonaDAO(responsavel_dao=resp_dao)
resp_ctrl = ResponsavelController(resp_dao, bomb_dao)
bomb_ctrl = BombonaController(bomb_dao, resp_dao)

# Testar cadastro
resp_ctrl.cadastrar_responsavel("12345678901", "João Silva", "11987654321", "LABORATÓRIO")
bomb_ctrl.cadastrar_bombona("LAB-001", 25.5, "ÁCIDO", "12345678901")

# Verificar resultados
print(resp_ctrl.listar_responsaveis())
print(bomb_ctrl.listar_bombonas())
```

## 📞 Próximos Passos

1. **Implementar Views**: Criar as telas de interface gráfica
2. **Melhorar UX**: Adicionar máscaras e validação em tempo real
3. **Relatórios Avançados**: Gráficos e exportação PDF
4. **Configurações**: Permitir personalização do sistema
5. **Deploy**: Preparar para distribuição

## 🤝 Contribuição

Este projeto é acadêmico, mas sugestões são bem-vindas:

1. Mantenha a arquitetura estabelecida
2. Siga os padrões de nomenclatura
3. Adicione testes para novas funcionalidades
4. Documente adequadamente o código
5. Respeite os princípios SOLID

## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais.

---

**Sistema desenvolvido com foco em boas práticas de Engenharia de Software** 🚀