# Atividade Gen Ai Rocket Lab 2026
Esse repositório contém a integração entre a minha plataforma fullstack de compras online e meu agente de ia __Text-To-SQL__. O agente permite que o usuário faça perguntas em linguagem natural sobre o banco de dados e receba respostas baseadas em consultas SQL exeutadas em tempo real.

---

## 🛠️ Tecnologias Utilizadas

### Backend (python)
- **FastAPI**: Framework web de alta performance.
- **Pydantic-AI**: Framework para criação de agentes com suporte a modelos estruturados (Gemini).
- **Google Gemini 2.0 Flash**: O cérebro por trás da análise de dados.
- **SQLite**: Banco de dados relacional para armazenamento das informações de e-commerce.

### Frontend (TypeScript)
- **React + TypeScript**: Base da interface.
- **Tailwind CSS**: Estilização baseada em utilitários.
- **Axios**: Cliente HTTP para comunicação com a API.
- **Lucide React**: Conjunto de ícones minimalistas.
  
---

## ❓ Onde está o agente no código?

```
📦 backend
  ┣ 📂 app
  ┃  ┣ 📂 agent
  ┃  ┃  ┗ 📂 agents
  ┃  ┃     ┣ 📜 agent.py -- Agente principal
  ┃  ┃     ┗ 📜 judge_agent.py -- Agente secundário não utilizado
  ┃  ┣ 📜 __init__.py
  ┃   ┗ 📜 main.py -- Main para realização de testes rápidos
  ...
  ┣ 📂 utils
     ┣ 📜 db.py -- Classe para auxiliar o agente a realizar as queryes
     ...
```

---

## 🏗️ Arquitetura do Sistema

O projeto é dividido em dois grandes blocos: um agente inteligente que "fala" SQL e uma interface de chat flutuante.

### O Agente (AI Engine)
O agente utiliza o seguinte fluxo:

1. Exploração: Lista e descreve tabelas para entender o schema.
2. Validação: Busca valores únicos em colunas de status ou categorias antes de filtrar (evita erros de grafia).
3. Execução: Gera e executa queries SQL seguras (apenas SELECT).
4. Conclusão: Formata os dados retornados em uma resposta textual estruturada.

### O Widget de Chat

Um componente React com posição fixa (`fixed`) e expansível para que o usuário interaja:

- Atualização Otimista: A mensagem do usuário aparece instantaneamente.
- Feedback Visual: Indicador de "Processando..." enquanto a IA consulta o banco.
- Design Responsivo: Adaptado para diferentes resoluções.

---

## 🚀 Como Executar o Backend

### Pré-requisitos
* Python 3.10+
* Ambiente virtual (venv)
* Chave de API do Google Gemini (configurada no arquivo .env)

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

## 📡 API Endpoints

### `POST /chat/`
Endpoint para enviar uma pergunta para o analista de dados

**Request Body:**
```JSON
{
  "question": "Quais foram os 5 produtos mais vendidos no mês passado?"
}
```

**Response**
```JSON
{
  "conclusion": "Os 5 produtos mais vendidos foram: 1. Teclado Pantera (50 unid), 2. Mouse Falcão (45 unid)..."
}
```

---

### 💡 Notas de Desenvolvimento
- **Somente Leitura**: Apenas comandos SELECT são permitidos.
- **Busca de Distintos**: É obrigatório checar valores reais antes de aplicar filtros de texto.
- **Limitação de Output**: Consultas exploratórias são limitadas a 30 linhas para evitar sobrecarga.
- **Uso do list_tables e outras ferramentas**: O agente não recebe o schema completo do banco de dados, invés disso ele recebe a lista de tabelas e precisa usar as ferramentas passadas para gerar o SQL, isso evita que o agente confiante demais com sua resposta e seja mais "curioso"
- **Criação do judge-agent**: Foi criando um agente secundário para julgar e avaliar as respostas do agente principal, mas o limite de tokens tornou ele inviável de ser usado.
