from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import PasswordResetRequest
from .serializers import (
    CustomTokenObtainPairSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, RequestResetSerializer, ApproveResetSerializer
)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
        
        # Mantém a sessão atualizada para o usuário
        update_session_auth_hash(request, user)
        
        return Response({"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)

class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = RequestResetSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            # Apagar requisições antigas pendentes para evitar duplicatas
            PasswordResetRequest.objects.filter(user=user, status='PENDING').delete()
            PasswordResetRequest.objects.create(user=user)
        return Response({"message": "Se o e-mail existir, a solicitação foi enviada aos administradores."}, status=status.HTTP_200_OK)

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class AdminPasswordResetRequestListView(generics.ListAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None

    def get_queryset(self):
        return PasswordResetRequest.objects.filter(status='PENDING').order_by('-created_at')

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
