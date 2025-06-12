# 📄 Gestão de Contratos

API para gerenciamento de contratos de crédito pessoal, construída com **Django Rest Framework**.

---

## 🚀 Como rodar com Docker

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/devAndreFC/gestao-contratos.git
cd gestao-contratos
```

### 2️⃣ Suba os containers com Docker Compose

```bash
docker compose up --build
```

🔐 A aplicação já cadastra o primeiro usuário automaticamente:

* 👤 **Usuário:** `admin`
* 🔒 **Senha:** `admin`

🔗 Acesse a aplicação em: [http://localhost:8000/](http://localhost:8000/)

---

## 🧪 Populando dados de exemplo

Para criar 20 contratos fictícios (com 10 parcelas cada), execute:

```bash
docker compose exec web python manage.py create_fake_contracts
```

---

## 📚 Documentação interativa

* 🌀 **Swagger:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
* 📘 **Redoc:** [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

---

## 🔐 Autenticação

* ⚙️ **Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
* 🛡️ **JWT Token:**

  * Obtenha o token em: `/api/token/`
  * Atualize o token em: `/api/token/refresh/`

> **Nota:** A API exige autenticação via **JWT** ou **sessão** para acessar rotas protegidas.

---

## ✅ Rodando os testes

Execute os testes com cobertura:

```bash
docker compose exec web coverage run manage.py test
```

Para gerar o relatório de cobertura em HTML:

```bash
docker compose exec web coverage html
```

📂 O relatório será gerado na pasta `htmlcov`.
Abra o arquivo `htmlcov/index.html` no navegador para visualizar os resultados.

---

## 👨‍💻 Autor

* [devAndreFC](https://github.com/devAndreFC)

