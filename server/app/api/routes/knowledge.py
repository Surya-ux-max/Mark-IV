"""Knowledge base search REST endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies.get_services import get_rag_engine

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


@router.get("/search")
async def search(
    q: str = Query(..., description="Search query", min_length=2),
    top_k: int = Query(2, ge=1, le=5),
    rag_engine=Depends(get_rag_engine),
) -> dict:
    """Search the knowledge base and return ranked documents."""
    docs = await rag_engine.retrieve(q, top_k=top_k)
    return {
        "query": q,
        "results": [
            {
                "doc_id": d.doc_id,
                "title": d.title,
                "category": d.category,
                "score": round(d.score, 3),
                "preview": d.content[:200],
            }
            for d in docs
        ],
    }


@router.get("/documents")
async def list_documents(
    rag_engine=Depends(get_rag_engine),
) -> dict:
    """List all loaded knowledge documents."""
    docs = await rag_engine.retrieve("", top_k=50)  # get all with low scores
    return {
        "total": rag_engine.document_count,
        "documents": [
            {"doc_id": d.doc_id, "title": d.title, "category": d.category}
            for d in rag_engine._documents
        ],
    }
