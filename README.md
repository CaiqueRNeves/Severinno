# Severinno

Plataforma de gestão acadêmica desenvolvida seguindo metodologia SCRUM. Este repositório contém o backend em Django Rest Framework e, futuramente, o frontend em React.

## Tecnologias
- Django 5 + Django REST Framework
- PostgreSQL (com fallback para SQLite em desenvolvimento)
- drf-spectacular para documentação OpenAPI/Swagger
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

Mais detalhes serão documentados nas próximas sprints.
