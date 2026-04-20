# Atividade Dev Rocket Lab 2026
Esse repositório contém minha plataforma fullstack de compras online. Ela foi criada seguindo os requisitos passados pela Visagio no seu bootcamp Rocket Lab 2026
e teve o design inspirado na [Fallen Store](https://www.fallenstore.com.br/), todos os créditos à eles por terem criado um design tão massa.

---

## 🗄️ Estrutura do Repositório
- `/backend`: API construída com FastAPI e SQLAlchemy.

- `/frontend`: Interface em React + Vite utilizando Tailwind CSS.

- `/csv-database-files`: Conjunto de dados inicial para o povoamento do banco.

---

## 🚀 Como Executar o Backend

### Pré-requisitos
* Python 3.10+
* Ambiente virtual (venv)

### Passo a Passo
1.  **Acesse o diretório:**
    ```
    cd backend
    ```
2.  **Crie e ative o ambiente virtual:**
    ```
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```
    pip install -r requirements.txt
    ```
4.  **Configuração do Banco de Dados (Alembic):**
    O projeto utiliza SQLite com suporte a `batch mode` para migrações complexas.
    ```
    alembic upgrade head
    ```
5.  **Povoamento (Seed):**
    Execute seu script de povoamento para ler os arquivos da pasta `/csv-database-files` e inserir no SQLite:
    ```
    python seed.py
    ```
6.  **Inicie o servidor:**
    ```
    python -m app.main
    ```
    * Acesse a documentação com _Swagger_ em: `http://localhost:8000/docs`

---

## 💻 Como Executar o Frontend

### Pré-requisitos
* Node.js (LTS recomendado)
* npm ou yarn

### Passo a Passo
1.  **Acesse o diretório:**
    ```
    cd frontend
    ```
2.  **Instale as dependências:**
    ```
    npm install
    ```
3.  **Inicie o servidor de desenvolvimento:**
    ```
    npm run dev
    ```
    * Acesse a aplicação em: `http://localhost:5173`

---

## 🛠️ Tecnologias Utilizadas

### Backend
* **FastAPI:** Framework para aplicações web Python.
* **SQLAlchemy:** ORM para manipulação do banco de dados.
* **Alembic:** Gestão de migrações (configurado para Cascade Delete no SQLite).
* **Pydantic:** Validação de dados e Schemas.

### Frontend
* **React + Vite:** Desenvolvimento de interfaces interativas.
* **Tailwind CSS:** Estilização baseada em utilitários.
* **Axios:** Consumo de APIs com tratamento de paginação e filtros.
* **TypeScript:** Tipagem estática para maior segurança no código.

---

### ⚙️ Funcionalidades
* Navegação entre todos os produtos com paginação
* Ao clicar no produto é possível ver todas as informações dele (preço, medida, nota média, vendas, comentários, etc)
* É possível pesquisar pelo nome e/ou pela categoria dos produtos
* Edição de produtos
* Criação de produtos novo
* É possível deletar um produto da base de dados 

---

### 💡 Notas de Desenvolvimento
* Para buscas de produtos, o frontend envia o parâmetro `nome` (ou `name`, conforme configurado na rota do FastAPI).
* O banco SQLite foi configurado com `render_as_batch=True` no Alembic para permitir alterações de Constraints e Foreign Keys sem perda de dados.
* Os produtos criados possuem preço 0 pois os valores dos produtos são baseados na sua última venda, como o produto não tem vendas ele tem valor de 0 R$

---

**Dica:** Antes de rodar o `seed.py`, certifique-se de que os caminhos dos arquivos CSV no script estão apontando corretamente para a pasta `../csv-database-files/`.
