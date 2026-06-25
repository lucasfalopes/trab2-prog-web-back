from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from devices.models import Device, Utensil

User = get_user_model()

DEVICES = [
    {'name': 'Monitor Cardíaco MC-200',  'device_type': 'Monitor',     'status': 'Disponível', 'location': 'UTI - Leito 1'},
    {'name': 'Ventilador Pulmonar VP-10','device_type': 'Ventilador',  'status': 'Em uso',     'location': 'UTI - Leito 3'},
    {'name': 'Bomba de Infusão BI-500',  'device_type': 'Bomba',       'status': 'Em uso',     'location': 'Enfermaria A'},
    {'name': 'Desfibrilador DEF-3000',   'device_type': 'Desfibrilador','status': 'Disponível','location': 'Pronto Socorro'},
    {'name': 'Oxímetro OX-100',          'device_type': 'Oxímetro',    'status': 'Manutenção', 'location': 'Almoxarifado'},
    {'name': 'Cadeira de Rodas CR-01',   'device_type': 'Mobilidade',  'status': 'Disponível', 'location': 'Recepção'},
    {'name': 'Eletrocardiógrafo ECG-7',  'device_type': 'Diagnóstico', 'status': 'Em uso',     'location': 'Cardiologia'},
    {'name': 'Nebulizador NEB-50',       'device_type': 'Respiratório','status': 'Manutenção', 'location': 'Manutenção'},
]

UTENSILS = [
    {'name': 'Bisturi Elétrico', 'utensil_type': 'Cirúrgico', 'quantity': 15, 'location': 'Centro Cirúrgico'},
    {'name': 'Luvas Cirúrgicas', 'utensil_type': 'EPI', 'quantity': 1000, 'location': 'Almoxarifado'},
    {'name': 'Pinça Kelly', 'utensil_type': 'Cirúrgico', 'quantity': 50, 'location': 'Sala de Sutura'},
]

USERS = [
    {
        'username': 'engenheiro',
        'email': 'engenheiro@hospmed.com',
        'password': 'Admin@12345',
        'role': 'ADMIN',
        'first_name': 'Carlos',
        'last_name': 'Engenheiro',
    },
    {
        'username': 'medico',
        'email': 'medico@hospmed.com',
        'password': 'Medico@12345',
        'role': 'CLINICAL',
        'first_name': 'Ana',
        'last_name': 'Médica',
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com usuários de teste'

    def handle(self, *args, **options):
        self._seed_users()
        self._seed_devices()
        self._seed_utensils()
        self.stdout.write(self.style.SUCCESS('Seed concluído com sucesso.'))

    def _seed_users(self):
        for data in USERS:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'role': data['role'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                },
            )
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(f"  Criado: {user.username} ({user.role})")
            else:
                self.stdout.write(f"  Já existe: {user.username} ({user.role})")

    def _seed_devices(self):
        for data in DEVICES:
            device, created = Device.objects.get_or_create(
                name=data['name'],
                defaults={
                    'device_type': data['device_type'],
                    'status': data['status'],
                    'location': data['location'],
                },
            )
            if created:
                self.stdout.write(f"  Criado dispositivo: {device.name} [{device.status}]")
            else:
                self.stdout.write(f"  Já existe dispositivo: {device.name}")

    def _seed_utensils(self):
        for data in UTENSILS:
            utensil, created = Utensil.objects.get_or_create(
                name=data['name'],
                defaults={
                    'utensil_type': data['utensil_type'],
                    'quantity': data['quantity'],
                    'location': data['location'],
                },
            )
            if created:
                self.stdout.write(f"  Criado utensílio: {utensil.name} [Qtd: {utensil.quantity}]")
            else:
                self.stdout.write(f"  Já existe utensílio: {utensil.name}")
