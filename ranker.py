# ranker.py
from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from embedder import embed_texts
from utils import top_keywords, extract_highlight_sentences, simple_clean

def rank_resumes(job_description: str, resumes: List[Dict[str, Any]], model: str = None):
    """
    resumes: list of dicts: {"filename": str, "text": str}
    Returns pandas DataFrame with columns: filename, score, matched_keywords, highlights, raw_text
    """
    # Clean
    jd = simple_clean(job_description)
    resume_texts = [simple_clean(r["text"]) for r in resumes]
    filenames = [r["filename"] for r in resumes]

    # Build small corpus: jd + resumes
    corpus = [jd] + resume_texts
    embeddings = embed_texts(corpus)
    jd_emb = np.array(embeddings[0]).reshape(1, -1)
    resume_embs = np.array(embeddings[1:])

    sims = cosine_similarity(dj_safe(jd_emb), dj_safe(resume_embs)).flatten()
    # if sims shape odd, fallback:
    if sims.shape[0] != len(resume_texts):
        sims = cosine_similarity(jd_emb, resume_embs).flatten()

    # Get keywords from JD
    jd_keywords = top_keywords(jd, top_k=50)

    rows = []
    for i, fname in enumerate(filenames):
        score = float(sims[i])  # 0..1 (cosine)
        matched = [k for k in jd_keywords if k in resume_texts[i].lower()]
        highlights = extract_highlight_sentences(resume_texts[i], matched, max_sentences=3)
        rows.append({
            "filename": fname,
            "score": round(score, 4),
            "matched_keywords": ", ".join(matched[:12]),
            "highlights": " | ".join(highlights),
            "raw_text": resume_texts[i]
        })

    df = pd.DataFrame(rows).sort_values(by="score", ascending=False).reset_index(drop=True)
    return df

def dj_safe(arr):
    # ensure 2D array float32
    import numpy as np
    a = np.array(arr).astype("float32")
    if a.ndim == 1:
        a = a.reshape(1, -1)
    return a
