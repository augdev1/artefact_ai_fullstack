# Emporio da Musica - AI Agent & Evaluation Harness

Projeto desenvolvido para a primeira fase do processo seletivo de AI Engineer Full Stack na Artefact.

Trata-se de uma solucao integrada para o atendimento ao cliente da loja ficticia Emporio da Musica (Campo Grande/MS), combinando agente conversacional baseado no padrao ReAct orquestrado via LangChain, RAG para consulta ao manual de politicas internas, pipeline de ETL para normalizacao e carga de dados relacionais, camada deterministica de seguranca (Guardrails de escopo), persistencia de sessoes de conversa e um Test & Evaluation Harness automatizado com benchmark de ground-truth.

---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/207afb92-ce5a-4682-8852-755aa828418a" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8fb68b38-0728-4a11-a44e-0a72e9c36b90" />

---


## 1. Arquitetura e Decisoes Tecnicas

A concepcao do projeto baseou-se em seis pilares fundamentais de engenharia de software e inteligencia artificial:

### 1.1. Orquestracao do Agente: LangChain com Padrao ReAct (LangGraph)
* **Abordagem**: Implementado utilizando `langgraph.prebuilt.create_react_agent`, o padrao moderno e recomendado no ecossistema LangChain.
* **Justificativa**: A arquitetura ReAct (Reasoning + Acting) permite que o modelo alterne ciclos de pensamento (*Thought*), acao (*Action*) e observacao (*Observation*), executando chamadas de funcoes com tipagem estrita via Pydantic (`@tool`). Isso viabiliza consultas combinadas complexas (por exemplo, consultar as politicas de pagamento e o estoque de um produto no mesmo turno de interacao), inspecionando cada etapa intermediaria do raciocinio.

### 1.2. Provedor de LLM e Resiliencia
* **Modelo Principal**: Google Gemini (`gemini-3.5-flash-lite`), acessado via `langchain-google-genai`.
* **Modelo de Contingencia**: OpenAI (`gpt-4o-mini`), configuravel via variaveis de ambiente.
* **Justificativa**: O `gemini-3.5-flash-lite` apresenta tempos de resposta sub-segundo, suporte nativo a function calling em lingua portuguesa e viabilidade economica para alto volume transacional de mensagens. O sistema foi desenhado de forma desacoplada, permitindo alternar de provedor ou modelo via arquivo `.env` sem alteracao de codigo de aplicacao. O projeto tambem disponibiliza um motor deterministico offline (`mock`) para fins de integracao continua (CI/CD) e testes sem consumo de creditos de API.

### 1.3. Tratamento de Dados (ETL) e Camada de Persistencia
* **Tratamento dos Dados (`app/db/etl.py`)**:
  * **Sanitizacao e Normalizacao de Texto**: Padronizacao Unicode via NFKC e higienizacao de espacos em branco.
  * **Conformidade Monetaria**: Conversao e arredondamento estrito de valores e percentuais de desconto para ponto flutuante de precisao fixa (duas casas decimais).
  * **Integridade de Estoque**: Validacao de limites nao-negativos (`stock_quantity >= 0`).
  * **Extracao de Especificacoes**: Validacao e parsing de strings JSON para dicionarios tipados de atributos tecnicos (madeiras, escala, captadores, etc.).
  * **Validacao de Campanhas Promocionais**: Separacao binaria estrita entre promocoes ativas (`is_active = 1`) e promocoes expiradas (`is_active = 0`), garantindo conformidade com a diretriz do manual de nunca aplicar descontos expirados.
* **Banco de Dados Relacional**:
  * Implementado em SQLite (`data/emporio.db`) com ativacao forcada de chaves estrangeiras (`PRAGMA foreign_keys = ON;`) e criacao de indices de busca (`idx_products_name`, `idx_products_category`, `idx_products_price`, `idx_orders_customer`, `idx_orders_tracking`).
  * **Persistencia de Conversas**: Tabela `conversation_history` indexada por `session_id`, garantindo que o contexto de atendimento de cada cliente seja preservado em disco mesmo entre reinicializacoes da aplicacao.
  * **Roadmap para PostgreSQL em Docker**: A camada de persistencia foi projetada para que a migracao do SQLite local para o PostgreSQL em ambiente conteinerizado via `docker-compose` ocorra sem impacto na camada de servico.

### 1.4. Arquitetura de Recuperacao de Politicas (RAG)
* **Fonte de Conhecimento**: Manual de Politicas e Procedimentos de Atendimento ao Cliente (`data/politicas_da_loja.pdf`, Versao 2.1).
* **Estrategia**: Estruturacao semantica categorizada por dominios especificos (horarios de expediente, endereco comercial, regras de devolucao e arrependimento pelo CDC em 7 dias, prazos de garantia de 90 dias, regras de frete e nao-cumulatividade do desconto PIX de 5% sobre promocoes).
* **Justificativa**: Evita alucinacoes de prazos e termos legais atraves de recuperacao deterministica focada nos trechos exatos do manual.

### 1.5. Guardrails Deterministicos de Escopo
* **Mapeamento de Restricoes**: Conforme estipulado no documento da loja, a Emporio da Musica comercializa **exclusivamente instrumentos musicais completos** e **nao comercializa acessorios avulsos** (cordas avulsas, encordoamentos, palhetas, cabos, pedais de efeito, amplificadores ou cases avulsos).
* **Implementacao (`app/agent/guardrails.py`)**: Uma camada de inspecao antes do envio a LLM intercepta consultas de acessorios ou topicos fora do escopo institucional (programacao, receitas, politica partidaria), emitindo recusa polida e direcionamento para lojas parceiras.
* **Beneficio**: Reducao de latencia, eliminacao de consumo de tokens em perguntas invalidas e garantia de 100% de precisao no cumprimento do escopo da loja.

### 1.6. Tecnologias e Stacks do Frontend
A interface visual do usuario foi desenvolvida para atender aos requisitos de responsividade, estetica moderna em tema escuro, persistencia de estado e navegabilidade fluida:
* **React 18**: Biblioteca base da Single Page Application (SPA), operando com hooks reativos (`useState`, `useEffect`, `useRef`, `useMemo`) para sincronizacao do historico de mensagens, gerenciamento de sessoes de chat e atualizacao otimista da interface.
* **TypeScript**: Tipagem estatica e definicao formal dos contratos de dados (`Message`, `ChatSession`, `ChatResponse`, `HealthResponse`), garantindo integridade e previsibilidade no consumo da API REST.
* **Tailwind CSS**: Framework utilitario para estilizacao e responsividade mobile-first, incluindo paleta customizada com o tom magenta institucional da Artefact (`#E60067`), classes de transicao para a barra lateral recolhivel (`w-72` / `w-0` com `overflow-hidden`) e design system escuro para componentes conversacionais.
* **Marked.js**: Motor de parsing e compilacao de Markdown para HTML em tempo de execucao, garantindo que respostas contendo catalogos, especificacoes tecnicas, precos e regras de parcelamento sejam renderizadas com alinhamento visual, listas estruturadas e tipografia limpa, sem caracteres crus de formatacao.
* **HTML5 LocalStorage API**: Camada de persistencia no navegador que preserva o identificador da sessao ativa e a listagem de conversas entre recarregamentos de pagina (F5), reconciliando os dados com o endpoint de historico do banco SQLite.
* **Vite & Tooling**: Configuracao de build no diretorio `frontend/` suportando compilacao rapida, hot-reload em ambiente de desenvolvimento e empacotamento para producao.
* **Identidade Visual e SVG Vetorial**: Recriacao grafica do logotipo **ARTEFACT** no topo da interface com espacamento uniforme (`tracking-[0.06em]`), glifos geometricos em chevron (`/\`) e linha de realce magenta, alem de iconografia dedicada para o usuario e o robo assistente.

---

## 2. Instrucoes de Configuracao e Execucao

### 2.1. Pre-requisitos
* Python 3.11 ou superior (desenvolvido e testado em Python 3.12).
* Gerenciador de pacotes `uv` (recomendado) ou `pip`.

### 2.2. Instalacao do Ambiente

```bash
# 1. Clonar o repositorio
git clone https://github.com/augdev1/artefact_ai_fullstack.git
cd artefact_ai_fullstack

# 2. Criar e ativar o ambiente virtual (com uv)
uv venv .venv
uv pip install -e ".[dev]"

# Alternativa com pip tradicional
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/MacOS:
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2.3. Configuracao de Variaveis de Ambiente

Copie o modelo de configuracao:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-3.5-flash-lite

# Configuracoes opcionais
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4o-mini
DATABASE_PATH=data/emporio.db
HOST=0.0.0.0
PORT=8000
```

### 2.4. Execucao do Servidor Full Stack

O backend FastAPI serve nativamente a aplicacao frontend React na rota raiz:

```bash
python -m app.main
```

Acesse os servicos:
* **Interface Web do Agente**: http://localhost:8000
* **Documentacao Interativa da API (Swagger UI)**: http://localhost:8000/docs
* **Healthcheck da API**: http://localhost:8000/api/health

---

## 3. Harness Engineering e Suite de Testes

O projeto conta com uma suite abrangente de 39 testes automatizados com `pytest` e um runner de benchmark sobre um dataset de referencia (*Golden Dataset*):

### 3.1. Execucao da Suite Completa (`pytest`)

```bash
pytest -v
```

Distribuicao da cobertura de testes:
* `tests/test_database.py`: Validacao do pipeline de ETL, contagens de registros e integridade referencial de chaves estrangeiras.
* `tests/test_tools.py`: Testes isolados de consultas com filtros de preco, consulta de itens especificos, calculo de descontos PIX e consulta de status de pedidos.
* `tests/test_guardrails.py`: 16 cenarios avaliando o bloqueio de solicitacoes de acessorios e assuntos fora de escopo, alem da liberacao de consultas legitimas de instrumentos.
* `tests/test_agent.py`: Testes do ciclo ReAct do agente, roteamento e persistencia de memoria multirrodada.
* `tests/test_api.py`: Integracao dos endpoints FastAPI (`/api/health`, `/api/chat`, `/api/chat/history/{sessionId}`).
* `tests/test_frontend.py`: Validacao de integracao da SPA React (carregamento HTML, elementos visuais de identidade Artefact e persistencia via LocalStorage).
* `tests/harness/test_harness.py`: Execucao automatizada das assercoes de ground-truth.

### 3.2. Execucao do Benchmark do Evaluation Harness

```bash
python tests/harness/run_eval.py
```

Resultados obtidos no benchmark:
* Total de Casos de Teste: 10
* Casos Aprovados: 10 / 10 (100.0%)
* Precisao dos Guardrails de Escopo: 3 / 3 (100.0%)
* Acuracia de Roteamento de Ferramentas: 7 / 7 (100.0%)
* Tempo Total de Execucao: 0.28 segundos

---

## 4. Exemplos de Interacao com o Agente

Conforme solicitado nas instrucoes do desafio, 5 conversas completas estao registradas no arquivo [`examples/conversations.md`](examples/conversations.md), cobrindo os seguintes cenarios:

1. **Consulta de catalogo com teto de preco**: "Quais opcoes de violoes disponiveis voces tem custando ate R$1000?" (Execucao de `search_products`).
2. **Consulta especifica e condicoes de pagamento**: "Quanto custa o Takamine GD20? Como funciona o pagamento parcelado e no PIX?" (Execucao de `get_product_details` e `get_store_policies`).
3. **Aplicacao de politicas de troca e arrependimento (CDC)**: "Comprei um teclado pelo site mas me arrependi da minha compra, chegou ontem. Posso devolver meu pedido?" (Execucao de `get_store_policies`).
4. **Acionamento de Guardrail de escopo**: "Voces vendem encordoamento de guitarra 0.10, palhetas Fender e amplificador de 50W?" (Bloqueio deterministico imediato e recusa polida com sugestao de lojas parceiras).
5. **Rastreamento de pedido com dados relacionais**: "Gostaria de saber o status do meu pedido 1. Quando chega?" (Execucao de `check_order_status`).

---

## 5. Limitacoes Conhecidas e Proximos Passos

1. **Migracao para PostgreSQL via Docker**:
   * *Estado Atual*: Persistencia em SQLite relacional com integridade referencial ativada.
   * *Plano*: Concluir a conteinerizacao da camada de dados utilizando uma imagem oficial de PostgreSQL no `docker-compose.yml`, suportando alta concorrencia e particionamento transacional de historicos de conversas.
2. **Busca Vetorial Densa (RAG Semantico Multimodal)**:
   * Implementacao de embeddings vetoriais (via `pgvector` ou Qdrant) para viabilizar consultas semanticas por sonoridade e estilos musicais (ex.: "violao com timbre aveludado para tocar jazz").
3. **Observabilidade e Tracing**:
   * Instrumentacao do pipeline com OpenTelemetry ou LangSmith para acompanhamento granular de latencia, custo por sessao e deteccao de desvios (*drift*).
4. **Canal WhatsApp e Audio**:
   * Integracao com API de mensageria oficial (WhatsApp Business API) e pipeline de transcricao de audio utilizando Whisper para mensagens de voz.

---

## 6. Uso de Assistentes de Codigo

Em conformidade com a exigencia de transparencia do processo seletivo:
* **Ferramenta Utilizada**: Antigravity AI Engineer (DeepMind / Gemini 3.8).
* **Metodologia de Workflow**:
  * Utilizado no formato de pair programming tecnico e aceleracao de produtividade.
  * O assistente atuou no auxilio a montagem dos schemas Pydantic, escrita do pipeline de ETL de normalizacao dos CSVs, criacao da bateria de testes unitarios e integracao do benchmark deterministico.
  * As decisoes de arquitetura (LangChain ReAct com LangGraph, guardrail deterministico pre-LLM, RAG estruturado sobre o manual da loja e estrategia de persistencia relacional) foram tomadas de acordo com as especificacoes do desafio.

---

## 7. Estrutura de Diretorios

```
artefact_ai_fullstack/
├── app/
│   ├── agent/
│   │   ├── guardrails.py       # Barreira de escopo (acessorios e off-topic)
│   │   ├── langchain_agent.py  # Agente ReAct LangChain (LangGraph)
│   │   ├── memory.py           # Gerenciador de persistencia de historico
│   │   └── persona.py          # Instrucoes de persona e diretrizes de resposta
│   ├── api/
│   │   ├── routes.py           # Endpoints REST FastAPI
│   │   └── server.py           # Aplicacao FastAPI e servidor de arquivos estaticos
│   ├── db/
│   │   ├── database.py         # Conexao e operacoes relacionais em SQLite
│   │   └── etl.py              # Pipeline ETL para limpeza e tipagem dos 6 CSVs
│   ├── knowledge/
│   │   └── policies.py         # Base de conhecimento RAG extraida do PDF
│   ├── static/
│   │   └── index.html          # SPA React responsiva com identidade Artefact
│   ├── tools/
│   │   ├── catalog_tools.py    # Consultas de catalogo, precos e promocoes
│   │   ├── langchain_tools.py  # Definicoes de ferramentas LangChain (@tool)
│   │   ├── order_tools.py      # Consulta de pedidos e rastreamento
│   │   └── policy_tools.py     # Ferramenta RAG de politicas da loja
│   ├── config.py               # Configuracoes de ambiente e settings
│   └── main.py                 # Ponto de entrada Uvicorn
├── data/
│   ├── *.csv                   # Bases operacionais fornecidas no desafio
│   ├── politicas_da_loja.pdf   # Manual interno de procedimentos
│   └── emporio.db              # Banco SQLite relacional pos-ETL
├── examples/
│   └── conversations.md        # 5 exemplos de interacao documentados
├── frontend/                   # Componentes React TypeScript complementares
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   └── types.ts
│   └── package.json
├── tests/
│   ├── harness/
│   │   ├── golden_dataset.json # Ground-truth de avaliacao
│   │   ├── run_eval.py         # Benchmark automatizado com tabela de metricas
│   │   └── test_harness.py     # Suite de validacao do harness
│   ├── test_agent.py           # Testes do agente e memoria
│   ├── test_api.py             # Testes dos endpoints HTTP
│   ├── test_database.py        # Testes de integridade de dados e SQL
│   ├── test_frontend.py        # Testes de integracao do frontend
│   ├── test_guardrails.py      # Testes da barreira de escopo
│   └── test_tools.py           # Testes das ferramentas de negocio
├── .env.example
├── pyproject.toml
└── README.md
```
