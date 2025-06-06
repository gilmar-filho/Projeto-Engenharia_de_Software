# responsavel/forms.py

from django import forms
from django.core.exceptions import ValidationError
from responsavel.models import Responsavel
from responsavel.factories.responsavel_factory import ResponsavelFactory


class ResponsavelForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de responsáveis.
    Integra com ResponsavelFactory para validações robustas.
    """
    
    cpf = forms.CharField(
        max_length=14,  # Para permitir formatação (XXX.XXX.XXX-XX)
        label='CPF',
        help_text='Digite apenas os números ou use o formato XXX.XXX.XXX-XX',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'pattern': r'[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2}',
            'title': 'Digite um CPF válido'
        })
    )
    
    nome = forms.CharField(
        max_length=100,
        label='Nome Completo',
        help_text='Digite o nome completo (mínimo: nome e sobrenome)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'João Silva Santos',
            'autocomplete': 'name'
        })
    )
    
    telefone = forms.CharField(
        max_length=15,  # Para permitir formatação (XX) XXXXX-XXXX
        label='Telefone',
        help_text='Digite apenas os números ou use o formato (XX) XXXXX-XXXX',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999',
            'pattern': r'\(?[0-9]{2}\)?\s?[0-9]{4,5}-?[0-9]{4}',
            'title': 'Digite um telefone válido'
        })
    )
    
    setor = forms.CharField(
        max_length=50,
        label='Setor',
        help_text='Setor de trabalho do responsável',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Laboratório de Química',
            'list': 'setores-sugeridos'
        })
    )
    
    class Meta:
        model = Responsavel
        fields = ['cpf', 'nome', 'telefone', 'setor']
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário com configurações personalizadas.
        """
        super().__init__(*args, **kwargs)
        
        # Se está editando um responsável existente, não permite alterar o CPF
        if self.instance and self.instance.pk:
            self.fields['cpf'].widget.attrs['readonly'] = True
            self.fields['cpf'].help_text = 'CPF não pode ser alterado após o cadastro'
    
    def clean_cpf(self):
        """
        Valida o CPF usando a ResponsavelFactory.
        
        Returns:
            str: CPF limpo e validado
            
        Raises:
            ValidationError: Se o CPF é inválido
        """
        cpf = self.cleaned_data.get('cpf')
        
        if not cpf:
            raise ValidationError('CPF é obrigatório.')
        
        try:
            cpf_limpo = ResponsavelFactory._validar_e_formatar_cpf(cpf)
            if not cpf_limpo:
                raise ValidationError('CPF inválido.')
        except Exception:
            raise ValidationError('CPF inválido.')
        
        # Verifica se já existe outro responsável com esse CPF (apenas em criação)
        if not self.instance.pk:  # Novo responsável
            if Responsavel.objects.filter(cpf=cpf_limpo).exists():
                raise ValidationError('Já existe um responsável cadastrado com este CPF.')
        
        return cpf_limpo
    
    def clean_nome(self):
        """
        Valida o nome usando a ResponsavelFactory.
        
        Returns:
            str: Nome validado e formatado
            
        Raises:
            ValidationError: Se o nome é inválido
        """
        nome = self.cleaned_data.get('nome')
        
        if not nome:
            raise ValidationError('Nome é obrigatório.')
        
        if not ResponsavelFactory._validar_nome(nome):
            raise ValidationError(
                'Nome inválido. Deve conter pelo menos nome e sobrenome, '
                'apenas letras e ter entre 2 e 100 caracteres.'
            )
        
        return nome.strip().title()
    
    def clean_telefone(self):
        """
        Valida o telefone usando a ResponsavelFactory.
        
        Returns:
            str: Telefone limpo e validado
            
        Raises:
            ValidationError: Se o telefone é inválido
        """
        telefone = self.cleaned_data.get('telefone')
        
        if not telefone:
            raise ValidationError('Telefone é obrigatório.')
        
        telefone_limpo = ResponsavelFactory._validar_e_formatar_telefone(telefone)
        if not telefone_limpo:
            raise ValidationError(
                'Telefone inválido. Deve ter 10 ou 11 dígitos '
                '(telefone fixo ou celular) com DDD válido.'
            )
        
        return telefone_limpo
    
    def clean_setor(self):
        """
        Valida o setor usando a ResponsavelFactory.
        
        Returns:
            str: Setor validado e formatado
            
        Raises:
            ValidationError: Se o setor é inválido
        """
        setor = self.cleaned_data.get('setor')
        
        if not setor:
            raise ValidationError('Setor é obrigatório.')
        
        if not ResponsavelFactory._validar_setor(setor):
            raise ValidationError(
                'Setor inválido. Deve ter entre 2 e 50 caracteres e '
                'conter apenas letras, números e alguns símbolos.'
            )
        
        return setor.strip().title()
    
    def save(self, commit=True):
        """
        Salva o responsável usando a ResponsavelFactory para garantir consistência.
        
        Args:
            commit (bool): Se deve salvar no banco imediatamente
            
        Returns:
            Responsavel: Instância do responsável criado/atualizado
        """
        if self.instance.pk:
            # Editando responsável existente
            responsavel = self.instance
            responsavel.setNome(self.cleaned_data['nome'])
            responsavel.setTelefone(self.cleaned_data['telefone'])
            responsavel.setSetor(self.cleaned_data['setor'])
        else:
            # Criando novo responsável
            try:
                responsavel = ResponsavelFactory.criar_responsavel(
                    cpf=self.cleaned_data['cpf'],
                    nome=self.cleaned_data['nome'],
                    telefone=self.cleaned_data['telefone'],
                    setor=self.cleaned_data['setor']
                )
            except ValueError as e:
                raise ValidationError(f'Erro ao criar responsável: {str(e)}')
        
        if commit:
            responsavel.save()
        
        return responsavel


class ResponsavelBuscaForm(forms.Form):
    """
    Formulário para busca de responsáveis com múltiplos filtros.
    """
    
    OPCOES_BUSCA = [
        ('', 'Selecione o tipo de busca'),
        ('cpf', 'CPF'),
        ('nome', 'Nome'),
        ('setor', 'Setor'),
        ('todos', 'Listar Todos'),
    ]
    
    tipo_busca = forms.ChoiceField(
        choices=OPCOES_BUSCA,
        required=True,
        label='Tipo de Busca',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'toggleBuscaField()'
        })
    )
    
    termo_busca = forms.CharField(
        max_length=100,
        required=False,
        label='Termo de Busca',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o termo para busca...'
        })
    )
    
    def clean(self):
        """
        Validação geral do formulário de busca.
        
        Returns:
            dict: Dados limpos e validados
            
        Raises:
            ValidationError: Se os dados são inconsistentes
        """
        cleaned_data = super().clean()
        tipo_busca = cleaned_data.get('tipo_busca')
        termo_busca = cleaned_data.get('termo_busca')
        
        # Se não é "todos", precisa de termo de busca
        if tipo_busca and tipo_busca != 'todos':
            if not termo_busca or not termo_busca.strip():
                raise ValidationError('Termo de busca é obrigatório para este tipo de busca.')
        
        # Validação específica por tipo
        if tipo_busca == 'cpf' and termo_busca:
            cpf_limpo = ResponsavelFactory._validar_e_formatar_cpf(termo_busca)
            if not cpf_limpo:
                raise ValidationError('CPF inválido para busca.')
            cleaned_data['termo_busca'] = cpf_limpo
        
        return cleaned_data


class ResponsavelDeleteForm(forms.Form):
    """
    Formulário para confirmação de exclusão de responsável.
    """
    
    confirmar_exclusao = forms.BooleanField(
        required=True,
        label='Confirmo que desejo excluir este responsável',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    cpf = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    def clean_confirmar_exclusao(self):
        """
        Valida a confirmação de exclusão.
        
        Returns:
            bool: True se confirmado
            
        Raises:
            ValidationError: Se não foi confirmado
        """
        confirmacao = self.cleaned_data.get('confirmar_exclusao')
        
        if not confirmacao:
            raise ValidationError('Você deve confirmar a exclusão.')
        
        return confirmacao