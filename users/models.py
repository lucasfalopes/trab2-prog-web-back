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

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
