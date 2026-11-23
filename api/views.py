from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from api.models import FundoImobiliario
from api.serializers import FundoImobiliarioSerializer


class FundoImobiliarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet que fornece automaticamente as ações padrão de um CRUD completo
    (Create, Read, Update, Delete) para o modelo FundoImobiliario.

    Aprimorado com os recursos dos capítulos 8 e 9 do e-book da Python Academy:
    - Filtros por campos específicos via DjangoFilterBackend (?codigo=...&setor=...)
    - Busca textual ampla via SearchFilter (?search=...)
    - Ordenação de resultados via OrderingFilter (?ordering=...)
    - Ordenação padrão por dividend_yield_medio_12m decrescente
    - Controle de permissões e autenticação do DRF
    """

    # 1. Consulta ao Banco (Queryset):
    queryset = FundoImobiliario.objects.all()

    # 2. Transformador de Dados (Serializer):
    serializer_class = FundoImobiliarioSerializer

    # 3. Controle de Acesso (Permissions):
    # Garante que apenas usuários autenticados acessem este ViewSet
    permission_classes = [permissions.IsAuthenticated]

    # 4. Processadores de Filtro, Busca e Ordenação:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Campos disponibilizados para filtragem exata (?codigo=...&setor=...)
    filterset_fields = ['codigo', 'setor']

    # Campos que permitem busca textual (?search=...)
    search_fields = ['codigo', 'setor']

    # Campos permitidos para ordenação dinâmica (?ordering=...)
    ordering_fields = [
        'dividend_yield_medio_12m',
        'setor',
        'vacancia_financeira',
        'vacancia_fisica',
        'quantidade_ativos',
        'data_constituicao',
    ]

    # Ordenação padrão aplicada quando nenhum parâmetro de ordenação for passado
    ordering = ['-dividend_yield_medio_12m']
