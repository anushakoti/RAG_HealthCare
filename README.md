# 🏥 RAG HealthCare — Agentic AI Medical Assistant

An intelligent healthcare assistant built with **Agentic RAG**, **LangGraph multi-agent workflows**, and **MCP (Model Context Protocol)** integrations. Powered by AWS Bedrock and ChromaDB, it answers patient queries, retrieves clinic FAQs, and schedules appointments — all through a Streamlit chat interface.

---

## What it does

- **FAQ mode** — answers questions about clinic hours, doctors, policies, and services using a RAG pipeline over a healthcare knowledge base
- **Full service mode** — connects to Composio MCP server to enable live appointment booking, doctor availability lookup, and scheduling workflows
- **Multi-agent orchestration** — LangGraph routes queries between a FAQ agent and a scheduling agent based on intent
- **Session memory** — maintains conversation context per patient session using LangGraph's built-in state management

---

## Architecture

```
User Query (Streamlit UI)
        │
        ▼
  LangGraph Router
   ┌────┴────┐
   │         │
FAQ Agent  Scheduling Agent
   │         │
ChromaDB   Composio MCP Server
(Vector    (Appointment Tools)
 Store)
   │         │
   └────┬────┘
        │
  AWS Bedrock (Claude / Titan)
        │
        ▼
   Chat Response
```

**Key components:**

| Folder | Purpose |
|--------|---------|
| `rag/` | Document ingestion, chunking, embedding, ChromaDB retrieval |
| `agents/` | FAQ agent and scheduling agent definitions |
| `graph/` | LangGraph workflow — `build_faq_only_workflow()` and `build_workflow()` |
| `tools/` | Tool definitions for MCP and agent function calling |
| `config/` | Environment and model configuration |
| `data/` | Healthcare knowledge base documents |
| `app.py` | Streamlit chat UI |
| `cli.py` | Command-line interface for testing |
| `demo.py` | Demo script with sample queries |

---

## Tech stack

- **LangChain** — RAG pipeline, document loaders, text splitters
- **LangGraph** — multi-agent workflow orchestration
- **AWS Bedrock** — LLM inference (Claude / Titan via `langchain-aws`)
- **ChromaDB** — vector store for healthcare document retrieval
- **MCP** — Composio MCP server for real-world appointment tool integration
- **LangSmith** — agent tracing and evaluation
- **Streamlit** — chat UI
- **FastAPI + Uvicorn** — optional API server
- **pypdf** — PDF document ingestion

---

## Getting started

### Prerequisites

- Python 3.11+
- AWS account with Bedrock access enabled
- Composio account (for full appointment booking mode)

### Installation

```bash
git clone https://github.com/anushakoti/RAG_HealthCare.git
cd RAG_HealthCare
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment setup

Create a `.env` file in the root directory:

```env
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# LangSmith (optional — for tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=rag-healthcare

# Composio MCP (optional — for full service mode)
COMPOSIO_API_KEY=your_composio_key
```

### Run the Streamlit app

```bash
streamlit run app.py
```

### Run via CLI

```bash
python cli.py
```

### Run the demo

```bash
python demo.py
```

---

## Usage

**Basic FAQ mode** (no MCP required):
> "What are your operating hours?"
> "Which specialists are available?"
> "Do you accept insurance?"

**Full service mode** (enable via sidebar → "Enable Full Services"):
> "Book me with Dr. Chen tomorrow at 10 AM"
> "What slots are available this week?"
> "Cancel my appointment for Friday"

---

## RAG pipeline

1. **Ingestion** — PDF and text healthcare documents loaded from `data/`
2. **Chunking** — `RecursiveCharacterTextSplitter` via `langchain-text-splitters`
3. **Embedding** — AWS Titan / Bedrock embeddings
4. **Vector store** — ChromaDB with persistent storage
5. **Retrieval** — similarity search with configurable `k` results
6. **Generation** — AWS Bedrock Claude with retrieved context injected into prompt

---

## Evaluation

Agent and RAG pipeline evaluation is implemented using **LangSmith**, tracking:
- Retrieval relevance
- Answer accuracy
- Latency per query



## License

MIT
