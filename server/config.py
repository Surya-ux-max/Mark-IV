import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Database configurations
SQLITE_DB_PATH = BASE_DIR / "survex.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")

# ChromaDB configurations
CHROMA_DIR = BASE_DIR / "chroma_db_data"

# LLM credentials
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")  # Change here if Groq deprecates this model

# Tools credentials
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", os.getenv("GITHUB_PAT", ""))
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Ensure directories exist
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
