# SaaS CRM (Multi-tenant) — ES/EN

## Español

CRM tipo SaaS con base “enterprise-ready” (auth, RBAC, migraciones, CI, Docker) y un dominio simple pero real:

- Organizaciones
- Leads
- IA opcional: “next best action” / resumen de lead vía `/api/v1/ai/chat`

### Endpoints
- `/api/v1/crm/orgs` (GET/POST)
- `/api/v1/crm/leads` (GET/POST)

### Run local

```bash
cp .env.example .env
docker compose up --build
```

---

## English

SaaS-style CRM with a portfolio-grade backend foundation and optional AI helper.

