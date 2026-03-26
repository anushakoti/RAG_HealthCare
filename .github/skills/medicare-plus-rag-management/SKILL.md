---
name: medicare-plus-rag-management
description: "Workflow for managing the RAG (Retrieval-Augmented Generation) knowledge base in MediCare Plus. Use when: adding new medical documents, updating existing records, or optimizing retrieval performance."
---

# MediCare Plus RAG Management

This skill guides the process of ingesting and maintaining the healthcare knowledge base used by the FAQ agent.

## Workflow: Ingesting New Documents

### 1. Prepare Documents
- Place all PDF files containing clinic information, policies, or doctor lists into the `data/` directory.
- Ensure the filenames are descriptive (e.g., `clinic_hours.pdf`, `insurance_providers.pdf`).

### 2. Configure Text Splitting
- Open `rag/ingest.py` and review the `split_text` function.
- **Default Config**: `chunk_size=500`, `chunk_overlap=200`.
- **Decision Point**: Increase `chunk_size` for dense documents, or decrease it for more granular retrieval.

### 3. Run Ingestion Script
Execute the ingestion script from the workspace root:
```powershell
python -m rag.ingest
```
This will:
1. Load all PDFs from `data/`.
2. Split them into chunks.
3. Store them in the `chroma_langchain_db/` vector store.

### 4. Optimize Retrieval
- Open `rag/retriever.py` and adjust the `top_k` parameter in `get_retriever()`.
- **Default Config**: `top_k=5`.
- **Decision Point**: Use a higher `top_k` (e.g., 7-10) if users report "missing information" in long documents.

### 5. Verify Ingestion
Use `demo.py` or `cli.py` to ask a question related to the newly added document.

## Maintenance Tasks

### Clearing the Knowledge Base
If you need to rebuild the database from scratch:
1. Delete the `chroma_langchain_db/` folder.
2. Re-run `python -m rag.ingest`.

### Updating Specific Files
- To update an existing document, replace the PDF in `data/` and re-run the ingestion. Note that Chroma adds documents; it doesn't automatically deduplicate by content unless specified. (Recommended: Clear and re-ingest for major updates).

## Quality Checklist
- [ ] PDFs are placed correctly in the `data/` folder.
- [ ] `rag/ingest.py` finishes without errors.
- [ ] `chroma_langchain_db/` directory contains `chroma.sqlite3`.
- [ ] The `faq_agent` successfully retrieves content from the new files.

## Completion Criteria
- New medical information is correctly stored in the vector database.
- The FAQ agent provides accurate answers based on the updated knowledge base.
