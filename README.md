# GeoPulse AI — Motor de GEO (Generative Engine Optimization) & AIO

O **GeoPulse AI** é um sistema completo e autônomo projetado para auditar, mensurar e otimizar a presença de empresas e marcas nos motores de busca generativa e assistentes inteligentes baseados em LLMs (**Perplexity, Google Gemini, OpenAI ChatGPT Search, Claude**).

---

## 🚀 Arquitetura & Stack Tecnológica
- **Backend:** Python 3.11+ com **FastAPI** assíncrono.
- **Banco de Dados:** **SQLite** com **SQLAlchemy 2.0 (Async)** e driver `aiosqlite`.
- **Frontend SPA:** Servida diretamente pelo FastAPI em `app/static/index.html` usando **HTML5, TailwindCSS (CDN) e Alpine.js**, com design Dark Mode profissional no padrão SaaS.
- **Extração Web:** Integração nativa gratuita com **Jina Reader (`r.jina.ai/{url}`)**, convertendo páginas em Markdown estruturado sem necessidade de chaves de scrapers pagas.
- **Auditoria de IA:** Suporte a chamadas diretas às APIs do **Google Gemini, OpenAI e Perplexity Sonar**, com **Motor de Simulação Analítica Realista** automático caso nenhuma chave esteja configurada.

---

## 📁 Estrutura do Projeto
```text
geopulse/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entrypoint FastAPI, rotas de API e SPA
│   ├── config.py            # Variáveis de ambiente com pydantic-settings
│   ├── database.py          # Conexão assíncrona SQLite + SQLAlchemy
│   ├── models.py            # Modelos Company, AuditRun, GeneratedAsset, SystemSetting
│   ├── schemas.py           # Validações Pydantic V2
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scraper.py       # Extração de site via Jina Reader (r.jina.ai)
│   │   ├── auditor.py       # Auditoria dos 3 Prompts Estratégicos (Share of Model)
│   │   └── generator.py     # Gerador de Schema JSON-LD, llms.txt, FAQ e Plano RAG
│   └── static/
│       └── index.html       # Dashboard SPA Dark Mode completo
├── .env.example
├── .env
├── requirements.txt
└── README.md
```

---

## 🛠️ Instalação e Execução

### 1. Criar ambiente virtual e instalar dependências
```bash
python -m venv venv
# No Windows PowerShell:
.\venv\Scripts\Activate.ps1
# No Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente (Opcional)
Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```
*(Você também pode configurar suas chaves do Gemini, OpenAI ou Perplexity diretamente pelo botão "Chaves de API" no topo do painel web, que as salvará no banco SQLite).*

### 3. Iniciar o Servidor
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Acesse o sistema no seu navegador em: **`http://localhost:8000`**

---

## 🎯 Entregáveis GEO Automáticos
Após submeter os dados de uma empresa, o GeoPulse AI gera automaticamente:
1. **Schema.org JSON-LD Híbrido:** Combinando `Organization`, `LocalBusiness` e `FAQPage`, com `sameAs`, `knowsAbout`, `areaServed` e `hasOfferCatalog`.
2. **Arquivo `/llms.txt`:** Padrão aberto canônico para leitura direta por crawlers de IA (`GPTBot`, `ClaudeBot`, `Google-Extended`, `PerplexityBot`).
3. **Bloco de FAQ Semântico (Zero-Click):** 5 perguntas e respostas com a resposta direta nas primeiras 30 palavras para extração imediata em sistemas RAG e AI Overviews.
4. **Plano de Co-ocorrência e Citação RAG Off-Page:** Checklist prático para criação de autoridade em entidades e artigos comparativos locais ("Top 5").
