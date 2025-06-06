# bombona/forms.py

from django import forms
from django.core.exceptions import ValidationError
from bombona.models import Bombona
from responsavel.models import Responsavel
from bombona.factories.bombona_factory import BombonaFactory


class BombonaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de bombonas.
    Integra com BombonaFactory para validações robustas.
    """
    
    codigo = forms.CharField(
        max_length=20,
        label='Código da Bombona',
        help_text='Código único da bombona (ex: D1423, AB123)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'D1423',
            'style': 'text-transform: uppercase;'
        })
    )
    
    volume = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        min_value=0.1,
        max_value=1000.0,
        label='Volume (Litros)',
        help_text='Volume da bombona em litros (0.1 a 1000L)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '25.50',
            'step': '0.01',
            'min': '0.1',
            'max': '1000'
        })
    )
    
    tipo_residuo = forms.CharField(
        max_length=100,
        label='Tipo de Resíduo',
        help_text='Tipo de resíduo químico armazenado',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ácido Sulfúrico',
            'list': 'tipos-residuos-sugeridos'
        })
    )
    
    responsavel = forms.ModelChoiceField(
        queryset=Responsavel.objects.all().order_by('nome'),
        label='Responsável',
        help_text='Selecione o responsável pela bombona',
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        empty_label='Selecione um responsável'
    )
    
    class Meta:
        model = Bombona
        fields = ['codigo', 'volume', 'tipo_residuo', 'responsavel']
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário com configurações personalizadas.
        """
        super().__init__(*args, **kwargs)
        
        # Se está editando uma bombona existente, não permite alterar o código
        if self.instance and self.instance.pk:
            self.fields['codigo'].widget.attrs['readonly'] = True
            self.fields['codigo'].help_text = 'Código não pode ser alterado após o cadastro'
        
        # Atualiza o queryset de responsáveis para incluir apenas ativos
        self.fields['responsavel'].queryset = Responsavel.objects.all().order_by('nome')
    
    def clean_codigo(self):
        """
        Valida o código usando a BombonaFactory.
        
        Returns:
            str: Código limpo e validado
            
        Raises:
            ValidationError: Se o código é inválido
        """
        codigo = self.cleaned_data.get('codigo')
        
        if not codigo:
            raise ValidationError('Código é obrigatório.')
        
        codigo_limpo = codigo.strip().upper()
        
        if not BombonaFactory._validar_codigo(codigo_limpo):
            raise ValidationError(
                'Código inválido. Deve conter letras e números, '
                'ter entre 1 e 20 caracteres (ex: D1423, AB123).'
            )
        
        # Verifica se já existe outra bombona com esse código (apenas em criação)
        if not self.instance.pk:  # Nova bombona
            if Bombona.objects.filter(codigo=codigo_limpo).exists():
                raise ValidationError('Já existe uma bombona cadastrada com este código.')
        
        return codigo_limpo
    
    def clean_volume(self):
        """
        Valida o volume usando a BombonaFactory.
        
        Returns:
            float: Volume validado
            
        Raises:
            ValidationError: Se o volume é inválido
        """
        volume = self.cleaned_data.get('volume')
        
        if volume is None:
            raise ValidationError('Volume é obrigatório.')
        
        if not BombonaFactory._validar_volume(float(volume)):
            raise ValidationError(
                'Volume inválido. Deve ser um número positivo '
                'entre 0.1 e 1000 litros com no máximo 2 casas decimais.'
            )
        
        return float(volume)
    
    def clean_tipo_residuo(self):
        """
        Valida o tipo de resíduo usando a BombonaFactory.
        
        Returns:
            str: Tipo de resíduo validado e formatado
            
        Raises:
            ValidationError: Se o tipo de resíduo é inválido
        """
        tipo_residuo = self.cleaned_data.get('tipo_residuo')
        
        if not tipo_residuo:
            raise ValidationError('Tipo de resíduo é obrigatório.')
        
        if not BombonaFactory._validar_tipo_residuo(tipo_residuo):
            raise ValidationError(
                'Tipo de resíduo inválido. Deve ser um tipo químico reconhecido '
                'com entre 2 e 100 caracteres.'
            )
        
        return tipo_residuo.strip().title()
    
    def clean_responsavel(self):
        """
        Valida o responsável selecionado.
        
        Returns:
            Responsavel: Responsável validado
            
        Raises:
            ValidationError: Se o responsável é inválido
        """
        responsavel = self.cleaned_data.get('responsavel')
        
        if not responsavel:
            raise ValidationError('Responsável é obrigatório.')
        
        if not isinstance(responsavel, Responsavel):
            raise ValidationError('Responsável inválido.')
        
        return responsavel
    
    def save(self, commit=True):
        """
        Salva a bombona usando a BombonaFactory para garantir consistência.
        
        Args:
            commit (bool): Se deve salvar no banco imediatamente
            
        Returns:
            Bombona: Instância da bombona criada/atualizada
        """
        if self.instance.pk:
            # Editando bombona existente
            bombona = self.instance
            bombona.setVolume(self.cleaned_data['volume'])
            bombona.setTipoResiduo(self.cleaned_data['tipo_residuo'])
            bombona.setResponsavel(self.cleaned_data['responsavel'])
        else:
            # Criando nova bombona
            try:
                bombona = BombonaFactory.criar_bombona(
                    codigo=self.cleaned_data['codigo'],
                    volume=self.cleaned_data['volume'],
                    tipo_residuo=self.cleaned_data['tipo_residuo'],
                    responsavel=self.cleaned_data['responsavel']
                )
            except ValueError as e:
                raise ValidationError(f'Erro ao criar bombona: {str(e)}')
        
        if commit:
            bombona.save()
        
        return bombona


class BombonaBuscaForm(forms.Form):
    """
    Formulário para busca de bombonas com múltiplos filtros.
    """
    
    OPCOES_BUSCA = [
        ('', 'Selecione o tipo de busca'),
        ('codigo', 'Código'),
        ('tipo_residuo', 'Tipo de Resíduo'),
        ('responsavel_nome', 'Nome do Responsável'),
        ('responsavel_cpf', 'CPF do Responsável'),
        ('volume_range', 'Faixa de Volume'),
        ('avancada', 'Busca Avançada'),
        ('todos', 'Listar Todas'),
    ]
    
    tipo_busca = forms.ChoiceField(
        choices=OPCOES_BUSCA,
        required=True,
        label='Tipo de Busca',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'toggleBuscaFields()'
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
    
    volume_min = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        label='Volume Mínimo (L)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.1',
            'step': '0.01'
        })
    )
    
    volume_max = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        label='Volume Máximo (L)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1000.0',
            'step': '0.01'
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
        volume_min = cleaned_data.get('volume_min')
        volume_max = cleaned_data.get('volume_max')
        
        # Validações específicas por tipo de busca
        if tipo_busca == 'volume_range':
            if volume_min is None or volume_max is None:
                raise ValidationError('Para busca por faixa de volume, informe os valores mínimo e máximo.')
            
            if volume_min > volume_max:
                raise ValidationError('Volume mínimo não pode ser maior que o volume máximo.')
        
        elif tipo_busca and tipo_busca not in ['todos', 'volume_range', 'avancada']:
            if not termo_busca or not termo_busca.strip():
                raise ValidationError('Termo de busca é obrigatório para este tipo de busca.')
        
        # Validação específica para CPF
        if tipo_busca == 'responsavel_cpf' and termo_busca:
            from responsavel.factories.responsavel_factory import ResponsavelFactory
            cpf_limpo = ResponsavelFactory._validar_e_formatar_cpf(termo_busca)
            if not cpf_limpo:
                raise ValidationError('CPF inválido para busca.')
            cleaned_data['termo_busca'] = cpf_limpo
        
        return cleaned_data


class BombonaDeleteForm(forms.Form):
    """
    Formulário para confirmação de exclusão de bombona.
    """
    
    confirmar_exclusao = forms.BooleanField(
        required=True,
        label='Confirmo que desejo excluir esta bombona',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    codigo = forms.CharField(
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


class BombonaTransferenciaForm(forms.Form):
    """
    Formulário para transferência de responsabilidade de bombona.
    """
    
    bombona_codigo = forms.CharField(
        max_length=20,
        label='Código da Bombona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )
    
    responsavel_atual = forms.CharField(
        max_length=100,
        label='Responsável Atual',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )
    
    novo_responsavel = forms.ModelChoiceField(
        queryset=Responsavel.objects.all().order_by('nome'),
        label='Novo Responsável',
        help_text='Selecione o novo responsável pela bombona',
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        empty_label='Selecione um responsável'
    )
    
    motivo_transferencia = forms.CharField(
        max_length=200,
        required=False,
        label='Motivo da Transferência',
        help_text='Opcional: descreva o motivo da transferência',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ex: Mudança de setor, aposentadoria, etc.'
        })
    )
    
    def clean_novo_responsavel(self):
        """
        Valida o novo responsável selecionado.
        
        Returns:
            Responsavel: Novo responsável validado
            
        Raises:
            ValidationError: Se o responsável é inválido
        """
        novo_responsavel = self.cleaned_data.get('novo_responsavel')
        
        if not novo_responsavel:
            raise ValidationError('Novo responsável é obrigatório.')
        
        return novo_responsavel