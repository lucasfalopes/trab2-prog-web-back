from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers as drf_serializers
from .models import PasswordResetRequest
from .serializers import (
    CustomTokenObtainPairSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, RequestResetSerializer, ApproveResetSerializer
)

User = get_user_model()


@extend_schema(
    tags=['Autenticação'],
    summary='Login — obtém tokens JWT',
    description=(
        'Autentica o usuário com username e senha. '
        'Retorna `access`, `refresh`, `role` (ADMIN ou CLINICAL), '
        '`username` e `must_change_password`.'
    ),
    responses={
        200: inline_serializer(
            name='LoginResponse',
            fields={
                'access': drf_serializers.CharField(),
                'refresh': drf_serializers.CharField(),
                'role': drf_serializers.ChoiceField(choices=['ADMIN', 'CLINICAL']),
                'username': drf_serializers.CharField(),
                'must_change_password': drf_serializers.BooleanField(),
            }
        ),
        401: OpenApiResponse(description='Credenciais inválidas'),
    }
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=['Usuários'],
    summary='Trocar senha (usuário logado)',
    description=(
        'Permite que o usuário autenticado altere sua própria senha. '
        'Requer o token JWT no header `Authorization: Bearer <token>`.'
    ),
    responses={
        200: OpenApiResponse(description='Senha alterada com sucesso'),
        400: OpenApiResponse(description='Senha atual incorreta ou dados inválidos'),
        401: OpenApiResponse(description='Não autenticado'),
    }
)
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": ["Senha atual incorreta."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.must_change_password = False
        user.save()

        update_session_auth_hash(request, user)

        return Response({"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Usuários'],
    summary='Solicitar recuperação de senha',
    description=(
        'Registra uma solicitação de recuperação de senha para o e-mail informado. '
        'A solicitação fica pendente até um administrador aprová-la em `/api/admin/reset-requests/`. '
        'Sempre retorna 200 para não revelar se o e-mail existe.'
    ),
    responses={
        200: OpenApiResponse(description='Solicitação registrada (independente de o e-mail existir)'),
    }
)
class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = RequestResetSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            PasswordResetRequest.objects.filter(user=user, status='PENDING').delete()
            PasswordResetRequest.objects.create(user=user)
        return Response({"message": "Se o e-mail existir, a solicitação foi enviada aos administradores."}, status=status.HTTP_200_OK)


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')


@extend_schema(
    tags=['Admin — Recuperação de Senha'],
    summary='Listar solicitações de reset pendentes',
    description=(
        'Retorna todas as solicitações de recuperação de senha com status PENDING. '
        'Restrito a usuários com perfil ADMIN.'
    ),
    responses={
        200: PasswordResetRequestSerializer(many=True),
        401: OpenApiResponse(description='Não autenticado'),
        403: OpenApiResponse(description='Sem permissão (requer perfil ADMIN)'),
    }
)
class AdminPasswordResetRequestListView(generics.ListAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None

    def get_queryset(self):
        return PasswordResetRequest.objects.filter(status='PENDING').order_by('-created_at')


@extend_schema(
    tags=['Admin — Recuperação de Senha'],
    summary='Aprovar ou recusar solicitação de reset',
    description=(
        'Processa uma solicitação de recuperação de senha pendente.\n\n'
        '- `APPROVE`: gera uma senha temporária aleatória, define `must_change_password=True` '
        'no usuário e retorna a senha no corpo da resposta para ser entregue manualmente.\n'
        '- `REJECT`: marca a solicitação como recusada.\n\n'
        'Restrito a usuários com perfil ADMIN.'
    ),
    responses={
        200: inline_serializer(
            name='ApproveResetResponse',
            fields={
                'message': drf_serializers.CharField(),
                'temporary_password': drf_serializers.CharField(required=False),
            }
        ),
        401: OpenApiResponse(description='Não autenticado'),
        403: OpenApiResponse(description='Sem permissão (requer perfil ADMIN)'),
        404: OpenApiResponse(description='Solicitação não encontrada ou não pendente'),
    }
)
class AdminApprovePasswordResetView(generics.GenericAPIView):
    serializer_class = ApproveResetSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, pk, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data['action']

        try:
            reset_req = PasswordResetRequest.objects.get(pk=pk, status='PENDING')
        except PasswordResetRequest.DoesNotExist:
            return Response({"error": "Solicitação não encontrada ou não pendente."}, status=status.HTTP_404_NOT_FOUND)

        if action == 'REJECT':
            reset_req.status = 'REJECTED'
            reset_req.save()
            return Response({"message": "Solicitação recusada com sucesso."})

        elif action == 'APPROVE':
            user = reset_req.user
            temp_password = get_random_string(length=12)
            user.set_password(temp_password)
            user.must_change_password = True
            user.save()

            reset_req.status = 'APPROVED'
            reset_req.save()

            return Response({
                "message": "Solicitação aprovada.",
                "temporary_password": temp_password
            })
