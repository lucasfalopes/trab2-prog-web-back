from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

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
