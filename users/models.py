from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Engenheiro/Administrador'),
        ('CLINICAL', 'Médico/Equipe Clínica'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CLINICAL',
        verbose_name='Perfil'
    )
    must_change_password = models.BooleanField(default=False)
    # Override para forçar unicidade — AbstractUser permite emails duplicados por padrão
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

class PasswordResetRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendente'),
        ('APPROVED', 'Aprovado'),
        ('REJECTED', 'Recusado'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reset para {self.user.username} - {self.status}"
