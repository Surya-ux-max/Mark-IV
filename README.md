# SurveX Mark IV — Virtual Robot Assistant Platform

> **Department of Computer Science & Engineering**  
> An interactive, real-time AI-powered virtual robot assistant featuring a 3D holographic background stage, dynamic CSS emotion rendering engine, WebSockets real-time event pipeline, voice speech synthesis/recognition, and Retrieval-Augmented Generation (RAG).

---

## 📋 Table of Contents

- [Overview & Features](#-overview--features)
- [System Architecture & Tech Stack](#-system-architecture--tech-stack)
- [Prerequisites & System Requirements](#-prerequisites--system-requirements)
- [🚀 Quick Start & Mounting Guide](#-quick-start--mounting-guide)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Backend Setup (`/server`)](#step-2-backend-setup-server)
  - [Step 3: Frontend Setup (`/client`)](#step-3-frontend-setup-client)
  - [Step 4: Verify Installation](#step-4-verify-installation)
- [⚙️ Environment Variables Reference](#%EF%B8%8F-environment-variables-reference)
- [🛠️ Zero-Error Troubleshooting Checklist](#%EF%B8%8F-zero-error-troubleshooting-checklist)
- [📂 Project Directory Structure](#-project-directory-structure)
- [🧪 Testing & Code Quality](#-testing--code-quality)
- [🤝 Contributor Guidelines](#-contributor-guidelines)
- [📄 License & Credits](#-license--credits)

---

## 🤖 Overview & Features

**SurveX Mark IV** (codenamed **Surya**) is an enterprise virtual robot designed for the CSE Department. It acts as an interactive assistant capable of natural dialogue, emotion expression, gesture/state management, and academic domain question-answering.

### Key Features
- **Dynamic 3D Holographic Stage**: Interactive canvas built with Three.js featuring particle fields, geometric lighting, and mouse-follow parallax.
- **18-Emotion Engine**: Real-time emotion rendering for the robot's face, eyes, and mouth (e.g., Happy, Thinking, Curious, Surprised, Neutral, Listening).
- **RAG Knowledge Base**: High-speed local RAG engine (`rapidfuzz`) powered by Markdown knowledge bases for instant departmental information retrieval.
- **LLM Integration**: High-throughput LLM reasoning via Groq Cloud (`llama-3.3-70b-versatile`).
- **Full-Duplex WebSockets**: Real-time event broadcasting for state machine changes, timeline actions, and voice synchronization.
- **Voice STT & TTS**: Built-in browser Web Speech API for voice commands and audio response synthesis.
- **Interactive Gestures**: Double-tap robot body to toggle Wake Up / Sleep modes.

---

## 🏗️ System Architecture & Tech Stack

```
                                ┌─────────────────────────────────────────┐
                                │             Web Browser                 │
                                │   React 19 + Vite 8 + Three.js Stage    │
                                └────────────────────┬────────────────────┘
                                                     │ WebSockets / HTTP
                                                     ▼
                                ┌─────────────────────────────────────────┐
                                │          FastAPI Backend Server         │
                                ├─────────────────────────────────────────┤
                                │ • Robot FSM & State Controller          │
                                │ • 18-Emotion Engine & Face/Hand Control │
                                │ • RAG Knowledge Search (RapidFuzz)      │
                                └───────────┬─────────────────┬───────────┘
                                            │                 │
                                            ▼                 ▼
                                    ┌───────────────┐ ┌───────────────┐
                                    │ Groq LLM API  │ │ Local KB Docs │
                                    │ (Llama 3.3)   │ │ (Markdown)    │
                                    └───────────────┘ └───────────────┘
```

### Technology Stack
* **Frontend (`/client`)**: React 19, Vite 8, Tailwind CSS v4, Three.js, HTML5 Web Speech API.
* **Backend (`/server`)**: Python 3.11+, FastAPI, Uvicorn, Pydantic v2, Structlog, RapidFuzz, WebSockets, Groq Python SDK.

---

## 💻 Prerequisites & System Requirements

Before setting up the project, ensure you have the following installed on your machine:

| Requirement | Minimum Version | Recommended Version | Download Link |
| :--- | :--- | :--- | :--- |
| **Node.js** | `v18.0.0` | `v20.x` or `v22.x` | [nodejs.org](https://nodejs.org/) |
| **npm** | `v9.0.0` | `v10.x` | Included with Node.js |
| **Python** | `v3.11.0` | `v3.11.x` or `v3.12.x` | [python.org](https://www.python.org/) |
| **Groq API Key** | Free Tier | Any | [console.groq.com](https://console.groq.com/) |
| **Git** | `v2.x` | Latest | [git-scm.com](https://git-scm.com/) |

---

## 🚀 Quick Start & Mounting Guide

Follow these step-by-step instructions to mount and launch the project without errors.

### Step 1: Clone the Repository

Open your terminal or command prompt and clone the repository:

```bash
git clone <repository-url>
cd "SurveX-mark IV"
```

---

### Step 2: Backend Setup (`/server`)

1. **Navigate to the server directory**:
   ```bash
   cd server
   ```

2. **Create a Python virtual environment**:
   - **Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate.bat
     ```

3. **Install Python dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -e .[dev]
   ```
   *(Note: `-e .[dev]` installs the project in editable mode along with development dependencies like pytest and httpx).*

4. **Configure Environment Variables**:
   Copy the example environment file `.env.example` to `.env`:
   - **Linux / macOS**:
     ```bash
     cp .env.example .env
     ```
   - **Windows (PowerShell)**:
     ```powershell
     Copy-Item .env.example .env
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     copy .env.example .env
     ```

   Open `.env` in your text editor and add your **Groq API Key**:
   ```ini
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```

5. **Start the Backend Server**:
   ```bash
   python main.py
   ```
   *Alternatively, run with Uvicorn directly*:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The backend server will start at `http://localhost:8000`. You should see log messages indicating `survex_robot_ready`.

---

### Step 3: Frontend Setup (`/client`)

Open a **new terminal window/tab** (keep the server running).

1. **Navigate to the client directory**:
   ```bash
   cd client
   ```

2. **Install Node.js packages**:
   ```bash
   npm install
   ```

3. **Start the Frontend Development Server**:
   ```bash
   npm run dev
   ```
   Vite will start the client web application at `http://localhost:5173`.

---

### Step 4: Verify Installation

1. Open your browser and navigate to **`http://localhost:5173`**.
2. Check the status badge on the UI:
   - Should display **STANDBY** (cyan color) once connected to WebSockets.
   - If it displays **CONNECTING TO SERVER...**, double check that the backend server on port `8000` is running.
3. Test interaction:
   - Click **WAKE UP** or **double-tap the robot body** to wake Surya up.
   - Click the **Microphone icon 🎤** or speak to interact with the virtual assistant.
4. Verify backend health endpoint:
   - Visit `http://localhost:8000/health` (should return `{"status": "ok"}`).
   - View Interactive API documentation at `http://localhost:8000/docs`.

---

## ⚙️ Environment Variables Reference

All backend configurations are loaded from `server/.env`. Below is a reference of available settings:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | *(Required)* | Your Groq Cloud API Key for LLM inference |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | LLM model name used for response generation |
| `ROBOT_NAME` | `Surya` | Primary display name for the virtual robot |
| `ROBOT_PERSONALITY` | `helpful, warm, curious...` | System prompt guidance for robot personality |
| `SERVER_HOST` | `0.0.0.0` | Host IP address for FastAPI server |
| `SERVER_PORT` | `8000` | Port for FastAPI backend |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `KNOWLEDGE_PATH` | `./knowledge` | Path to Markdown knowledge base files |
| `TOP_K_DOCS` | `2` | Top N RAG documents retrieved per prompt |
| `MAX_HISTORY_TURNS` | `10` | Conversation memory turn limit |
| `CORS_ORIGINS` | `http://localhost:5173...` | Comma-separated list of allowed CORS origins |

---

## 🛠️ Zero-Error Troubleshooting Checklist

If you run into issues during mounting or execution, check these common fixes:

### 1. `GROQ_API_KEY missing or invalid`
- **Symptom**: Server crashes on startup with authentication or missing API key error.
- **Fix**: Ensure `server/.env` exists and contains a valid key starting with `gsk_`. Get a key from [Groq Console](https://console.groq.com/).

### 2. Windows PowerShell `.venv` Script Execution Error
- **Symptom**: `File ...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`
- **Fix**: Run PowerShell as Administrator or execute the following in your session:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  ```

### 3. Python Version Mismatch (`< 3.11`)
- **Symptom**: Syntax errors or import errors regarding modern typing (`from __future__ import annotations`).
- **Fix**: Verify your Python version with `python --version`. Upgrade to Python `3.11.x` or `3.12.x`.

### 4. CORS Connection Refused in Browser
- **Symptom**: Browser console shows `Access to fetch at ... blocked by CORS policy`.
- **Fix**: Check `CORS_ORIGINS` in `server/.env`. Ensure `http://localhost:5173` is listed.

### 5. WebSocket Connection Failure (`ws://localhost:8000/ws`)
- **Symptom**: UI stuck on `CONNECTING TO SERVER...`.
- **Fix**: Ensure port `8000` is not blocked by a firewall or occupied by another application. Test `http://localhost:8000/health` in your browser.

### 6. Port Already in Use (`8000` or `5173`)
- **Symptom**: `OSError: [Errno 98] Address already in use` or Vite selecting port `5174`.
- **Fix**: Kill any hanging processes running on port 8000/5173, or update `SERVER_PORT` in `.env`.

---

## 📂 Project Directory Structure

```text
SurveX-mark IV/
├── readme.md                # Main repository documentation (this file)
├── client/                  # Frontend React + Vite Web Application
│   ├── index.html           # HTML entry point
│   ├── package.json         # Node dependencies & scripts
│   ├── vite.config.js       # Vite configuration with React compiler & Tailwind
│   ├── public/              # Static assets
│   └── src/
│       ├── App.jsx          # Main application component & layout
│       ├── main.jsx         # React DOM entry point
│       ├── index.css        # Global CSS & theme styles
│       ├── components/      # UI & Robot Components
│       │   ├── Background3D.jsx # Three.js holographic particle stage
│       │   ├── RobotBody.jsx    # Full robot body & posture stage
│       │   ├── RobotFace.jsx    # Face container & emotion rendering
│       │   ├── RobotEyes.jsx    # Eye expressions & gaze tracking
│       │   └── RobotMouth.jsx   # Mouth shape & speech keyframes
│       └── hooks/           # Custom React Hooks
│           ├── useRobot.js      # Robot state & emotion dispatching
│           ├── useSpeech.js     # Web Speech API (STT & TTS)
│           └── useWebSocket.js  # Real-time WebSocket connection manager
└── server/                  # Backend FastAPI Robot Platform
    ├── main.py              # Server launcher entry point
    ├── pyproject.toml       # Python dependencies & build config
    ├── .env.example         # Template environment variables
    ├── .python-version      # Target Python version (3.11)
    ├── knowledge/           # Markdown knowledge documents for RAG
    │   ├── mission.md
    │   ├── vision.md
    │   └── ...
    └── app/                 # FastAPI Application Core
        ├── main.py          # FastAPI application factory & lifecycle
        ├── animation/       # Face, Hand, Leg, & Timeline controllers
        ├── api/             # REST endpoints (health, chat, robot, knowledge)
        ├── brain/           # Conversation management & LLM logic
        ├── config/          # Settings & Pydantic config management
        ├── core/            # Logging, registry, & base utilities
        ├── emotion/         # 18-emotion state machine & intensity engine
        ├── events/          # Event dispatcher & sub/pub subscriptions
        ├── memory/          # RAG engine & turn-history buffer
        └── robot/           # Robot FSM state machine & controller
```

---

## 🧪 Testing & Code Quality

### Backend Testing (Python)
Run pytest tests inside the `server/` directory:

```bash
cd server
pytest
```

### Frontend Code Quality (ESLint)
Run ESLint check inside the `client/` directory:

```bash
cd client
npm run lint
```

---

## 🤝 Contributor Guidelines

We welcome contributions to SurveX Mark IV! Please follow these guidelines:

### Branching Strategy
1. Fork the repository and create a new feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/issue-description
   ```

### Code Standards
- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines. Use type annotations on all function signatures.
- **JavaScript/React**: Use modern React 19 functional components and custom hooks. Follow standard JSX formatting rules.

### Expanding the Knowledge Base
To add or update departmental information for RAG retrieval:
1. Navigate to `server/knowledge/`.
2. Add a new `.md` file (or update an existing one) containing clear markdown headings and text.
3. Restart the server (`python main.py`) so the RAG engine indexes the updated markdown files on startup.

### Submitting a Pull Request
1. Ensure all tests and linting checks pass cleanly.
2. Provide a descriptive title and summary of your changes in the Pull Request.
3. Include screenshots or screen recordings if adding visual or UI features.

---

## 📄 License & Credits

- **Department**: Computer Science & Engineering
- **Project**: SurveX Mark IV (Surya AI Virtual Robot)
- **Built with**: React, FastAPI, Groq LLM, Three.js, and Python.

---

<p align="center">Made with ❤️ by the CSE Department Team</p>
