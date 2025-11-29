# ResumeScreening Agent

## Overview
**ResumeScreening Agent** ranks candidate resumes against a job description using semantic embeddings and returns a ranked list with short explainability (matched skills and highlight sentences). Built as a rapid demo for Rooman’s AI Agent Development Challenge.

This project supports three embedding backends (choose one in `embedder.py`):
- **Local (recommended for free demos):** `sentence-transformers` (all-MiniLM-L6-v2)
- **Google Gemini** (requires `GEMINI_API_KEY` in `.env`)
- **OpenAI** (requires `OPENAI_API_KEY` in `.env`) — only if you have billing

## Demo
- Local Streamlit UI: `streamlit run app.py`  
- (Optional) Hosted link: Add once deployed to Streamlit Cloud / Render / Railway.

## Features
- Upload Job Description (paste/upload) and multiple resumes (PDF/DOCX/TXT).
- Extracts text from resumes using `pdfplumber` and `python-docx`.
- Generates embeddings and ranks resumes by cosine similarity.
- Displays matched keywords, highlight sentences, similarity score.
- Export ranked results as CSV.
- Configurable embedding backend for cost-free or cloud-run demos.

## Architecture
(See `assets/architecture.mmd` for Mermaid diagram or open the Mermaid text in README)

## Techstack & APIs used
- **UI:** Streamlit
- **Parsing:** pdfplumber, python-docx
- **Embeddings:** sentence-transformers (local) *or* Google Gemini *or* OpenAI embeddings (configurable)
- **Similarity & Ranking:** scikit-learn cosine similarity, pandas
- **Extras:** python-dotenv for secrets, simple CSV export

## Files
- `app.py` — Streamlit UI and control flow
- `embedder.py` — Embedding wrapper (switchable backends)
- `parser.py` — Resume parsing utilities
- `ranker.py` — Ranking & explainability logic
- `utils.py` — Helper functions (tokenization, highlights)
- `requirements.txt`
- `assets/architecture.mmd` — Mermaid architecture diagram
- `sample_resumes/` — Add sample resumes (PDF/DOCX/TXT)

## Setup & Run (local)
1. Clone repo:
   ```bash
   git clone <your-repo-url>
   cd resume-screening-agent
