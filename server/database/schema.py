# SQL schemas for normalized database tables in PostgreSQL and SQLite dialects

POSTGRES_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        profile TEXT,
        preferences TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        session_id VARCHAR(100) PRIMARY KEY,
        username VARCHAR(100) DEFAULT 'surya',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        summary TEXT,
        metadata TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(100) NOT NULL,
        role VARCHAR(50) NOT NULL,
        input_type VARCHAR(50) DEFAULT 'text',
        output_type VARCHAR(50) DEFAULT 'both',
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS agents (
        agent_id VARCHAR(100) PRIMARY KEY,
        metadata TEXT,
        status VARCHAR(50) DEFAULT 'ACTIVE',
        configuration TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS agent_executions (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(100) NOT NULL,
        agent_id VARCHAR(100) NOT NULL,
        execution_logs TEXT,
        runtime REAL,
        status VARCHAR(50),
        selected_tools TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS supervisor_decisions (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(100) NOT NULL,
        intent TEXT,
        selected_agents TEXT,
        reasoning TEXT,
        token_usage INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS short_term_memory (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(100) UNIQUE NOT NULL,
        context TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS long_term_memory (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        embedding_ref VARCHAR(200),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS settings (
        id SERIAL PRIMARY KEY,
        theme VARCHAR(50) DEFAULT 'dark',
        voice VARCHAR(50) DEFAULT 'default',
        language VARCHAR(50) DEFAULT 'en'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        task_desc TEXT NOT NULL,
        is_completed INTEGER DEFAULT 0,
        schedule TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cache_metadata (
        cache_key VARCHAR(200) PRIMARY KEY,
        source VARCHAR(100),
        content TEXT,
        expiration TIMESTAMP,
        invalidation_status INTEGER DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS calendar_events (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL
    )
    """
]

SQLITE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        profile TEXT,
        preferences TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        username TEXT DEFAULT 'surya',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        summary TEXT,
        metadata TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        input_type TEXT DEFAULT 'text',
        output_type TEXT DEFAULT 'both',
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS agents (
        agent_id TEXT PRIMARY KEY,
        metadata TEXT,
        status TEXT DEFAULT 'ACTIVE',
        configuration TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS agent_executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        agent_id TEXT NOT NULL,
        execution_logs TEXT,
        runtime REAL,
        status TEXT,
        selected_tools TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS supervisor_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        intent TEXT,
        selected_agents TEXT,
        reasoning TEXT,
        token_usage INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS short_term_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE NOT NULL,
        context TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS long_term_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        embedding_ref TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT DEFAULT 'dark',
        voice TEXT DEFAULT 'default',
        language TEXT DEFAULT 'en'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_desc TEXT NOT NULL,
        is_completed INTEGER DEFAULT 0,
        schedule TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cache_metadata (
        cache_key TEXT PRIMARY KEY,
        source TEXT,
        content TEXT,
        expiration DATETIME,
        invalidation_status INTEGER DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS calendar_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL
    )
    """
]
