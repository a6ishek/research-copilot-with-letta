
import os, uuid
from typing import List, Dict, Any, Optional, Tuple
from .memory_manager import sqlite_conn
from sentence_transformers import SentenceTransformer
import numpy as np

try:
    import faiss
    _HAS_FAISS = True
except Exception:
    _HAS_FAISS = False

EMBED_MODEL = "all-MiniLM-L6-v2"
_embedder = None
_index = None
_id_to_meta: Dict[int, Dict[str, Any]] = {}

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder

def chunk_text(t: str, size: int = 900, overlap: int = 150) -> List[str]:
    tokens = t.split()
    out = []
    i = 0
    while i < len(tokens):
        out.append(" ".join(tokens[i:i+size]))
        i += size - overlap
    return out

def ingest_text(title: str, text: str):
    conn = sqlite_conn(); cur = conn.cursor()
    doc_id = str(uuid.uuid4())
    cur.execute("INSERT OR REPLACE INTO documents (id,path,title,created_at) VALUES (?,?,?,?)",
                (doc_id, title, title, ""))
    conn.commit()
    chunks = chunk_text(text)
    for i, ch in enumerate(chunks):
        cid = str(uuid.uuid4())
        cur.execute("INSERT OR REPLACE INTO chunks (id,doc_id,chunk_index,text) VALUES (?,?,?,?)",
                    (cid, doc_id, i, ch))
    conn.commit()
    return doc_id, len(chunks)

def rebuild_index():
    global _index, _id_to_meta
    conn = sqlite_conn(); cur = conn.cursor()
    cur.execute("SELECT text, doc_id, chunk_index FROM chunks ORDER BY doc_id, chunk_index")
    rows = cur.fetchall()
    if not rows:
        _index = None
        _id_to_meta = {}
        return 0
    texts = [r[0] for r in rows]
    metas = [{"doc_id": r[1], "chunk_index": int(r[2]), "text": r[0]} for r in rows]
    emb = get_embedder().encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    if _HAS_FAISS:
        dim = emb.shape[1]
        idx = faiss.IndexFlatIP(dim)
        faiss.normalize_L2(emb)
        idx.add(emb)
        _index = idx
        _id_to_meta = {i:m for i,m in enumerate(metas)}
        return len(texts)
    else:
        _index = None
        _id_to_meta = {i:m for i,m in enumerate(metas)}
        return len(texts)

def search(query: str, k: int = 5):
    if _index is None and not _id_to_meta:
        return []
    q = get_embedder().encode([query], convert_to_numpy=True, normalize_embeddings=True)
    if _index is not None:
        D,I = _index.search(q, k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1: continue
            results.append((float(score), _id_to_meta.get(int(idx), {})))
        return results
    else:
        all_texts = [m['text'] for m in _id_to_meta.values()]
        all_embs = get_embedder().encode(all_texts, convert_to_numpy=True, normalize_embeddings=True)
        sims = (all_embs @ q[0]).tolist()
        indexed = list(_id_to_meta.items())
        scored = sorted([(sims[i], v) for i,(k,v) in enumerate(indexed)], key=lambda x: -x[0])[:k]
        return [(float(s), meta) for s, meta in scored]
