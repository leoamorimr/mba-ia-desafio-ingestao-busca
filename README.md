# Desafio MBA Engenharia de Software com IA - Full Cycle

## Sobre o Projeto

Sistema de RAG (Retrieval-Augmented Generation) para ingestão e busca de documentos PDF utilizando embeddings vetoriais e PostgreSQL com extensão pgvector.

## Arquitetura

O projeto é composto por três módulos principais:

- **`ingest.py`**: Responsável pela ingestão de documentos PDF, processamento de texto e armazenamento de embeddings
- **`search.py`**: Implementa a busca semântica utilizando similaridade de embeddings
- **`chat.py`**: Interface de chat que permite fazer perguntas sobre o documento ingerido

## Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Chaves de API:
  - OpenAI API Key
  - Google API Key (opcional)

## Configuração

### 1. Configuração do Ambiente

Copie o arquivo de exemplo e configure as variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_EMBEDDING_MODEL='models/embedding-001'
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL='text-embedding-3-small'
OPENAI_MODEL='gpt-5-nano'
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=gpt5_documents
PDF_PATH=document.pdf
```

### 2. Configuração do Banco de Dados

Inicie o PostgreSQL com pgvector usando Docker Compose:

```bash
docker-compose up -d
```

Este comando irá:
- Iniciar um container PostgreSQL com a extensão pgvector
- Criar automaticamente a extensão vector no banco de dados
- Configurar o banco `rag` na porta 5432

### 3. Ambiente Python

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

### 1. Ingestão de Documentos

Para processar e ingerir um documento PDF:

```bash
python src/ingest.py
```

Este comando irá:
- Carregar o PDF especificado em `PDF_PATH`
- Dividir o documento em chunks de 1000 caracteres
- Gerar embeddings usando OpenAI
- Armazenar os embeddings no PostgreSQL com pgvector

### 2. Busca e Chat

Para fazer perguntas sobre o documento ingerido:

**Modo interativo:**
```bash
python src/chat.py
```

**Modo comando direto:**
```bash
python src/chat.py "Sua pergunta aqui"
```

## Funcionalidades

### Ingestão (`ingest.py`)
- Carrega documentos PDF usando PyPDFLoader
- Processa texto com RecursiveCharacterTextSplitter
- Gera embeddings com OpenAI
- Armazena vetores no PostgreSQL com pgvector

### Busca (`search.py`)
- Busca semântica por similaridade de embeddings
- Filtra resultados por score de relevância (< 0.8)
- Utiliza LLM para gerar respostas baseadas no contexto
- Implementa regras rígidas para evitar alucinações

### Chat (`chat.py`)
- Interface simples para interação
- Suporte a argumentos de linha de comando
- Tratamento de erros robusto

## Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py          # Módulo de ingestão
│   ├── search.py          # Módulo de busca
│   └── chat.py            # Interface de chat
├── docker-compose.yml     # Configuração PostgreSQL + pgvector
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── document.pdf          # Documento de exemplo
└── README.md             # Documentação
```

## Troubleshooting

### Erro de conexão com banco de dados
Verifique se o PostgreSQL está rodando:
```bash
docker-compose ps
```

### Erro de API Key
Verifique se as chaves estão configuradas corretamente no arquivo `.env`

### Documento não encontrado
Verifique se o caminho em `PDF_PATH` está correto e o arquivo existe

## Tecnologias Utilizadas

- **LangChain**: Framework para aplicações com LLM
- **OpenAI**: Embeddings e modelo de linguagem
- **PostgreSQL + pgvector**: Banco vetorial
- **PyPDF**: Processamento de documentos PDF
- **Docker**: Containerização do banco de dados