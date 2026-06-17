from django.db import models


class Device(models.Model):
    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Em uso', 'Em uso'),
        ('Manutenção', 'Manutenção'),
    ]

    name        = models.CharField(max_length=200, verbose_name='Nome')
    device_type = models.CharField(max_length=100, verbose_name='Tipo')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível', verbose_name='Status')
    location    = models.CharField(max_length=200, verbose_name='Localização')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'

    def __str__(self):
        return f"{self.name} ({self.status})"
