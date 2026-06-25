# Sistema de Gerenciamento de Ativos Hospitalares - Backend

- Lucas Lopes - 2220647
- Diogo Marassi - 2220354

## Escopo do Projeto
Este projeto é o Backend de um sistema de gerenciamento de dispositivos médicos e ativos de um hospital. Desenvolvido inteiramente em Django (sem uso de templates HTML/CSS, seguindo o requisito), ele provê uma API RESTful completa para atender o Frontend.
O sistema conta com endpoints protegidos por JWT e diferentes níveis de permissão.

## O que foi desenvolvido
* **CRUD de Dispositivos:** Endpoints completos para criar, listar, atualizar e deletar dispositivos médicos.
* **Autenticação:** Sistema de login seguro com JWT.
* **Gerência de Senhas:** Fluxo de "esqueci minha senha" onde o usuário solicita a troca e um administrador (Engenheiro) aprova no painel e define uma senha temporária.
* **Controle de Acesso:** Diferentes visões do sistema. Engenheiros possuem privilégios administrativos (aprovação de reset de senhas, CRUD total) enquanto Médicos possuem acesso restrito aos dispositivos.
* **Documentação OpenAPI (Swagger):** Integração com `drf-spectacular` para documentar todas as rotas e facilitar o uso.

## Como Instalar e Rodar Localmente (Instruções de Uso)

### Pré-requisitos
* Python 3.9+
* uv (gerenciador de pacotes - ou pip)

### Passos
1. Clone o repositório:
   ```bash
   git clone <LINK_DO_REPO_BACKEND>
   cd trab2-prog-web-back
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   uv venv --python /usr/bin/python3
   source .venv/bin/activate
   ```

3. Instale as dependências (já devidamente fixadas para não haver conflitos):
   ```bash
   uv pip install -r requirements.txt
   ```

4. Aplique as migrações no banco de dados SQLite e crie os dados iniciais:
   ```bash
   python manage.py migrate
   python manage.py seed
   ```

5. Rode o servidor local:
   ```bash
   python manage.py runserver
   ```

6. Acesse a documentação da API no seu navegador: `http://localhost:8000/api/docs/`

### Testando a API
Os usuários de teste criados pelo script `seed` são:
* **Engenheiro (Admin):** `username`: `engenheiro` | `password`: `Admin@12345`
* **Médico:** `username`: `medico` | `password`: `Medico@12345`

## Manual do Usuário
* Ao acessar a rota `/api/docs/`, você visualizará a documentação interativa gerada pelo Swagger.
* Lá, o usuário/desenvolvedor pode expandir qualquer rota, ler sobre os parâmetros necessários, e testar diretamente.
* Para acessar endpoints restritos (como os de Dispositivos), utilize a rota `/api/token/` para gerar o par JWT. Clique no botão **Authorize** (cadeado) na interface do Swagger e insira o seu token JWT para realizar requisições autenticadas.

## Funcionalidades Testadas (Testes Manuais Realizados)

### O que funcionou (Testado e Aprovado)
* Login de usuário e geração de token JWT.
* Restrição de acesso em endpoints protegidos (401 Unauthorized retornado corretamente caso o acesso seja anônimo).
* Solicitação de "Esqueci a Senha" via fluxo de aprovação administrativo (Engenheiro) no backend.
* Todas as 4 operações (CRUD) da API de dispositivos funcionando de acordo.
* Documentação no Swagger UI renderizando perfeitamente todos os *schemas*.

### O que não funcionou
* O envio automático de e-mail com link de reset de senha foi cogitado inicialmente, mas, devido a limitações de configuração e chaves de servidor SMTP em ambientes de nuvem variados, optamos por não implementar o disparo de e-mails reais. A funcionalidade foi plenamente substituída com sucesso por um painel onde o administrador aprova manualmente as solicitações. Relatamos isso como escolha de design.