"""RAG engine — orchestrates document retrieval and context injection.

This is the primary entry point for the knowledge retrieval subsystem.
"""

from __future__ import annotations

from typing import List, Tuple

from app.core.interfaces import IKnowledgeRetriever
from app.core.logging import get_logger
from app.memory.rag.context_builder import build_context_block, get_source_titles
from app.memory.rag.document_loader import load_documents
from app.memory.rag.query_matcher import rank_documents
from app.models.knowledge import Document

logger = get_logger(__name__)


class RAGEngine(IKnowledgeRetriever):
    """Lightweight retrieval-augmented generation engine.

    Loads all markdown knowledge files into memory at startup and uses
    keyword + fuzzy scoring for fast, dependency-free retrieval.
    """

    def __init__(self, knowledge_path: str, top_k: int = 2) -> None:
        self._knowledge_path = knowledge_path
        self._top_k = top_k
        self._documents: List[Document] = []
        self._initialized = False

    async def initialize(self) -> None:
        """Load all knowledge documents into memory."""
        self._documents = await load_documents(self._knowledge_path)
        self._initialized = True
        logger.info(
            "rag_engine_ready",
            documents=len(self._documents),
            path=self._knowledge_path,
        )

    async def shutdown(self) -> None:
        self._documents.clear()
        self._initialized = False

    async def retrieve(self, query: str, top_k: int | None = None) -> List[Document]:
        """Retrieve top-k most relevant documents for a query."""
        if not self._initialized:
            raise RuntimeError("RAGEngine not initialized. Call initialize() first.")

        k = top_k or self._top_k
        ranked = rank_documents(query, self._documents)
        top = ranked[:k]

        logger.debug(
            "rag_retrieved",
            query=query[:60],
            results=[{"doc": d.doc_id, "score": round(d.score, 3)} for d in top],
        )
        return top

    async def get_context(self, query: str) -> Tuple[str, List[str]]:
        """Retrieve context block and source titles for LLM injection.

        Returns:
            (context_block_str, source_title_list)
        """
        docs = await self.retrieve(query)
        context = build_context_block(docs)
        sources = get_source_titles(docs)
        return context, sources

    @property
    def document_count(self) -> int:
        return len(self._documents)
