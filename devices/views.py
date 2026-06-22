from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .models import Device
from .serializers import DeviceSerializer
from users.permissions import IsAdminOrEngineer


@extend_schema_view(
    list=extend_schema(
        tags=['Dispositivos'],
        summary='Listar dispositivos',
        description=(
            'Retorna a lista de todos os dispositivos hospitalares cadastrados. '
            'Qualquer usuário autenticado pode acessar. '
            'Suporta filtros via query params.'
        ),
        parameters=[
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtra por status. Valores aceitos: `Disponível`, `Em uso`, `Manutenção`.',
                enum=['Disponível', 'Em uso', 'Manutenção'],
                required=False,
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Busca por nome ou tipo do dispositivo (case-insensitive).',
                required=False,
            ),
        ],
        responses={
            200: DeviceSerializer(many=True),
            401: OpenApiResponse(description='Não autenticado'),
        }
    ),
    create=extend_schema(
        tags=['Dispositivos'],
        summary='Criar dispositivo',
        description='Cria um novo dispositivo hospitalar. **Restrito a perfil ADMIN.**',
        responses={
            201: DeviceSerializer,
            400: OpenApiResponse(description='Dados inválidos'),
            401: OpenApiResponse(description='Não autenticado'),
            403: OpenApiResponse(description='Sem permissão (requer perfil ADMIN)'),
        }
    ),
    retrieve=extend_schema(
        tags=['Dispositivos'],
        summary='Detalhar dispositivo',
        description='Retorna os dados de um dispositivo específico. Qualquer usuário autenticado pode acessar.',
        responses={
            200: DeviceSerializer,
            401: OpenApiResponse(description='Não autenticado'),
            404: OpenApiResponse(description='Dispositivo não encontrado'),
        }
    ),
    update=extend_schema(
        tags=['Dispositivos'],
        summary='Atualizar dispositivo (PUT)',
        description='Atualização completa de um dispositivo. Todos os campos são obrigatórios. **Restrito a perfil ADMIN.**',
        responses={
            200: DeviceSerializer,
            400: OpenApiResponse(description='Dados inválidos'),
            401: OpenApiResponse(description='Não autenticado'),
            403: OpenApiResponse(description='Sem permissão (requer perfil ADMIN)'),
            404: OpenApiResponse(description='Dispositivo não encontrado'),
        }
    ),
    partial_update=extend_schema(
        tags=['Dispositivos'],
        summary='Atualizar dispositivo (PATCH)',
        description='Atualização parcial de um dispositivo. Apenas os campos enviados são alterados. **Restrito a perfil ADMIN.**',
        responses={
            200: DeviceSerializer,
            400: OpenApiResponse(description='Dados inválidos'),
            401: OpenApiResponse(description='Não autenticado'),
            403: OpenApiResponse(description='Sem permissão (requer perfil ADMIN)'),
            404: OpenApiResponse(description='Dispositivo não encontrado'),
        }
    ),
    destroy=extend_schema(
        tags=['Dispositivos'],
        summary='Excluir dispositivo',
        description='Remove permanentemente um dispositivo. **Restrito a perfil ADMIN.**',
        responses={
            204: OpenApiResponse(description='Excluído com sucesso'),
            401: OpenApiResponse(description='Não autenticado'),
            403: OpenApiResponse(description='Sem permissão (requer perfil ADMIN)'),
            404: OpenApiResponse(description='Dispositivo não encontrado'),
        }
    ),
)
class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.all()

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(device_type__icontains=search)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrEngineer()]
        return [IsAuthenticated()]
