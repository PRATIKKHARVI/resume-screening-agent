# utils.py
import re
from collections import Counter
import nltk

# ensure required NLTK data
nltk_packages = ["punkt", "stopwords", "wordnet", "omw-1.4"]
for pkg in nltk_packages:
    try:
        nltk.data.find(pkg)
    except LookupError:
        nltk.download(pkg)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

STOPWORDS = set(stopwords.words("english"))

def simple_clean(text: str) -> str:
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def top_keywords(text: str, top_k: int = 30):
    text = text.lower()
    tokens = [re.sub(r"[^a-z0-9#+]", "", t) for t in word_tokenize(text)]
    tokens = [t for t in tokens if t and t not in STOPWORDS and len(t) > 1]
    freq = Counter(tokens)
    common = [w for w, _ in freq.most_common(top_k)]
    return common

def extract_highlight_sentences(resume_text: str, keywords: list, max_sentences: int = 3):
    resume_text = simple_clean(resume_text)
    sents = sent_tokenize(resume_text)
    hits = []
    for s in sents:
        sl = s.lower()
        for k in keywords:
            if k in sl:
                hits.append(s.strip())
                break
        if len(hits) >= max_sentences:
            break
    return hits
