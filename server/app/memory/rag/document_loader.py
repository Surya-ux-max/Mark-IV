"""Document loader — reads and parses all knowledge markdown files.

Supports YAML frontmatter extraction for metadata (title, category, keywords).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

import aiofiles

from app.core.logging import get_logger
from app.models.knowledge import Document

logger = get_logger(__name__)

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_YAML_FIELD_RE = re.compile(r"^(\w[\w_-]*):\s*(.+)$", re.MULTILINE)
_YAML_LIST_ITEM_RE = re.compile(r"^\s+-\s+(.+)$", re.MULTILINE)


def _parse_frontmatter(raw: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body. Returns (metadata, body)."""
    match = _FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw.strip()

    fm_block = match.group(1)
    body = raw[match.end():].strip()
    metadata: dict = {}

    # Simple key: value extraction
    for field_match in _YAML_FIELD_RE.finditer(fm_block):
        key = field_match.group(1).lower()
        value = field_match.group(2).strip()
        if value.startswith("["):
            # Inline list: [a, b, c]
            items = [v.strip().strip('"\'') for v in value.strip("[]").split(",")]
            metadata[key] = [i for i in items if i]
        else:
            metadata[key] = value

    # Block list items (YAML list with - prefix)
    in_keywords = False
    keywords: List[str] = []
    for line in fm_block.splitlines():
        stripped = line.strip()
        if stripped.startswith("keywords:"):
            in_keywords = True
            continue
        if in_keywords:
            item_match = _YAML_LIST_ITEM_RE.match(line)
            if item_match:
                keywords.append(item_match.group(1).strip())
            elif stripped and not stripped.startswith("-"):
                in_keywords = False

    if keywords:
        metadata["keywords"] = keywords

    return metadata, body


async def load_documents(knowledge_path: str) -> List[Document]:
    """Asynchronously load all .md files from the knowledge directory."""
    path = Path(knowledge_path)
    if not path.exists():
        logger.error("knowledge_path_not_found", path=str(path))
        return []

    documents: List[Document] = []
    md_files = sorted(path.glob("*.md"))

    for md_file in md_files:
        try:
            async with aiofiles.open(md_file, mode="r", encoding="utf-8") as f:
                raw = await f.read()

            metadata, body = _parse_frontmatter(raw)
            doc = Document(
                doc_id=md_file.stem,
                title=metadata.get("title", md_file.stem.replace("-", " ").title()),
                category=metadata.get("category", "General"),
                short_name=metadata.get("short_name"),
                keywords=metadata.get("keywords", []),
                content=body,
                file_path=str(md_file),
            )
            documents.append(doc)
            logger.info("document_loaded", doc_id=doc.doc_id, title=doc.title)

        except Exception as exc:
            logger.error("document_load_failed", file=str(md_file), error=str(exc))

    logger.info("knowledge_base_loaded", total_documents=len(documents))
    return documents
