import chromadb
from config import CHROMA_DIR

# Initialize client defensively
try:
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
except Exception as e:
    print(f"Failed to initialize Persistent ChromaDB: {e}. Utilizing EphemeralClient.")
    chroma_client = chromadb.EphemeralClient()

# Get or create collection
try:
    collection = chroma_client.get_or_create_collection("survex_memory")
except Exception as e:
    print(f"Collection creation issue: {e}")
    collection = None

def save_semantic_memory(content, doc_id):
    if collection is None:
        return "Memory storage offline."
    try:
        collection.add(
            documents=[content],
            ids=[doc_id]
        )
        return "Memory stored in ChromaDB."
    except Exception as e:
        return f"Error saving semantic memory: {e}"

def search_semantic_memories(query, limit=3):
    if collection is None:
        return []
    try:
        results = collection.query(
            query_texts=[query],
            n_results=limit
        )
        # Parse output documents list
        docs = results.get("documents", [])
        return docs[0] if docs else []
    except Exception as e:
        print(f"Error querying semantic memories: {e}")
        return []
