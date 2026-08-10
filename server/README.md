# SurveX Mark IV — Server Backend

FastAPI-powered virtual robot backend server for SurveX Mark IV.

## Quick Start

1. **Virtual Environment & Dependencies**:
   ```bash
   python -m venv .venv
   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   # Linux/macOS: source .venv/bin/activate
   pip install -e .[dev]
   ```

2. **Environment File**:
   Copy `.env.example` to `.env` and configure your `GROQ_API_KEY`:
   ```bash
   cp .env.example .env
   ```

3. **Run Server**:
   ```bash
   python main.py
   ```

For full documentation, system architecture, environment variable specifications, and contributor guidelines, please see the [Main Project README](../readme.md).
