# Gestão de Contratos

API para gerenciamento de contratos de crédito pessoal, construída em Django + Django Rest Framework.

---

## 🚀 Como rodar com Docker

1️⃣ **Clone o repositório:**

```bash
git clone https://github.com/devAndreFC/gestao-contratos.git
cd gestao-contratos
```

2️⃣ **Suba os containers com Docker Compose:**

```bash
docker compose up --build
```

A API estará disponível em:  
👉 [http://localhost:8000/](http://localhost:8000/)

---

## 🛠️ Documentação interativa

- Swagger: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)  
- Redoc: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

---

## 🔐 Autenticação

- **Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)  
- **JWT Token:**  
  - Obtenha um token em: `/api/token/` (usuário + senha)  
  - Atualize o token em: `/api/token/refresh/`  

**OBS**: A API exige autenticação por JWT ou por sessão para acessar as rotas protegidas.

---


## ⚙️ Populando dados de exemplo

Crie 20 contratos fictícios (com 10 parcelas cada):

```bash
docker compose exec web python manage.py create_fake_contracts

```

No shell interativo, rode:

```python
from contratos.management.commands.populate_data import Command
Command().handle()
```
Para rodar os testes:
docker compose exec web coverage run manage.py test

Para ter acesso ao html do coverage:
docker compose exec web coverage html
---

**Autor:** [devAndreFC](https://github.com/devAndreFC)
