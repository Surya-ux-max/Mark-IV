"""Query matcher — scores documents against a user query.

Scoring algorithm:
  1. Keyword overlap: count how many document keywords appear in the query
  2. Title match: rapidfuzz partial_ratio of query vs document title
  3. Content match: rapidfuzz partial_ratio of query vs first 300 chars of content
  4. Weighted sum → final score in [0, 1]
"""

from __future__ import annotations

from typing import List

from rapidfuzz import fuzz

from app.models.knowledge import Document


def _normalize(text: str) -> str:
    return text.lower().strip()


def score_document(query: str, doc: Document) -> float:
    """Return a relevance score [0.0, 1.0] for a document given a query."""
    query_lower = _normalize(query)
    query_tokens = set(query_lower.split())

    # ── 1. Keyword overlap ────────────────────────────────────────────────────
    doc_keywords = [_normalize(kw) for kw in doc.keywords]
    # Also tokenize the title
    title_tokens = set(_normalize(doc.title).split())
    all_doc_tokens = set(doc_keywords) | title_tokens

    if all_doc_tokens:
        overlap = len(query_tokens & all_doc_tokens) / len(all_doc_tokens)
    else:
        overlap = 0.0

    # ── 2. Title fuzzy match ──────────────────────────────────────────────────
    title_score = fuzz.partial_ratio(_normalize(doc.title), query_lower) / 100.0

    # ── 3. Content partial match (first 400 chars) ────────────────────────────
    content_snippet = _normalize(doc.content[:400])
    content_score = fuzz.partial_ratio(content_snippet, query_lower) / 100.0

    # ── 4. Short name exact match bonus ──────────────────────────────────────
    short_name_bonus = 0.0
    if doc.short_name and _normalize(doc.short_name) in query_lower:
        short_name_bonus = 0.3

    # ── Weighted sum ──────────────────────────────────────────────────────────
    score = (
        overlap * 0.35
        + title_score * 0.30
        + content_score * 0.20
        + short_name_bonus
    )

    return min(score, 1.0)


def rank_documents(query: str, documents: List[Document]) -> List[Document]:
    """Score all documents and return them sorted by descending relevance."""
    scored: List[Document] = []
    for doc in documents:
        s = score_document(query, doc)
        doc_copy = doc.model_copy(update={"score": s})
        scored.append(doc_copy)

    return sorted(scored, key=lambda d: d.score, reverse=True)
