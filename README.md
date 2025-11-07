# Severinno

Plataforma de gestão acadêmica desenvolvida seguindo metodologia SCRUM. Este repositório contém o backend em Django Rest Framework e, futuramente, o frontend em React.

## Tecnologias
- Django 5 + Django REST Framework
- PostgreSQL (com fallback para SQLite em desenvolvimento)
- drf-spectacular para documentação OpenAPI/Swagger
- djangorestframework-simplejwt para autenticação JWT
- GitHub Actions para CI (testes + lint básico)

## Estrutura de pastas
```
Severinno/
├── backend/        # Projeto Django + apps
├── frontend/       # Aplicação React (será construída nas próximas sprints)
├── requirements.txt
└── README.md
```

## Preparação do ambiente
1. Crie um arquivo `.env` na raiz com base no `.env.example`.
2. (Opcional) Suba um banco PostgreSQL local e ajuste as variáveis `POSTGRES_*`.
3. Crie e ative um ambiente virtual e instale as dependências:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Executar o backend
1. Aplique as migrações:
   ```bash
   source venv/bin/activate
   python backend/manage.py migrate
   ```
2. Rode o servidor de desenvolvimento:
   ```bash
   python backend/manage.py runserver
   ```
3. Endpoints importantes:
   - `GET /api/health/` — verificação rápida de saúde da API.
   - `GET /api/docs/` — documentação interativa (Swagger UI).
   - `POST /api/accounts/register/` — cadastro de novos usuários (email + matrícula).
   - `POST /api/accounts/login/` — obtenção de tokens JWT (access + refresh).
   - `POST /api/accounts/refresh/` — renovação do access token.
   - `GET /api/accounts/me/` — dados do usuário autenticado (Bearer token obrigatório).
   - `GET /admin/` — painel administrativo personalizado (login requerido).
   - `GET/POST /api/rooms/` — CRUD de salas (apenas administradores).
   - `GET/POST /api/machines/` — CRUD de máquinas com especificações técnicas.
   - `GET/POST /api/reservations/` — reservas para professores (listagem restrita por perfil).
   - `POST /api/reservations/{id}/cancel/` — cancelamento permitido apenas antes do horário inicial.
   - `GET /api/reservations/available/?date=YYYY-MM-DD&start_time=HH:MM&end_time=HH:MM` — checagem de disponibilidade.
   - `GET/POST /api/software-requests/` — solicitações de software vinculadas a reservas (professores).
   - `PATCH /api/software-requests/{id}/status/` — atualização de status (apenas administradores).
   - `POST /api/accounts/logout/` — invalida o refresh token via blacklist (requer autenticação).

## Painel administrativo
- Header customizado com identidade visual da Severinno.
- Proxy `Professor` no Django Admin para CRUD exclusivo de docentes, exibindo foto, e-mail e matrícula.
- Admin forms garantem que professores sejam sempre do tipo correto, evitando inconsistências.

## Testes
Execute todos os testes automatizados com:
```bash
source venv/bin/activate
python backend/manage.py test
```

## Segurança já aplicada
- Configurações via `.env`.
- CORS configurado para o frontend.
- Middleware de Content Security Policy (CSP).
- Cabeçalhos HTTP seguros ativados para evitar sniffing/XSS.
- Autenticação JWT com tempos configuráveis via `JWT_ACCESS_LIFETIME_MINUTES` e `JWT_REFRESH_LIFETIME_DAYS`.
- Modelo de usuário customizado com autenticação por email e campos institucionais (matrícula, tipo de usuário e foto).
- Painel administrativo com branding próprio, filtros específicos e CRUD dedicado para professores.
- API protegida para cadastro de salas/máquinas e regras de reserva com validação de conflitos.
- Fluxo de solicitação de software com controle de status e validação de permissão.
- Autenticação JWT com refresh rotativo + blacklist (logout seguro) e throttling configurável.
- Regras de segurança avançadas ativadas em produção (HSTS, SSL redirect, cookies HttpOnly, CSP).

Mais detalhes serão documentados nas próximas sprints.
