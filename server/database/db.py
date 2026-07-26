import os
import sqlite3
import psycopg
from psycopg.rows import dict_row
from config import DATABASE_URL, SQLITE_DB_PATH
from database.schema import POSTGRES_TABLES, SQLITE_TABLES

def get_db_connection():
    if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://"):
        conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        return conn
    else:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    tables_list = POSTGRES_TABLES if is_postgres else SQLITE_TABLES
    for query in tables_list:
        cursor.execute(query)
        
    conn.commit()
    conn.close()

# 1. Message logs operations
def save_chat_message(session_id, role, content, input_type="text", output_type="both"):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    # Auto-initialize session if not exists
    create_session_if_not_exists(session_id)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO messages (session_id, role, input_type, output_type, content) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
        (session_id, role, input_type, output_type, content)
    )
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT role as sender, content as message, timestamp FROM messages WHERE session_id = {placeholder} ORDER BY id ASC LIMIT 100",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "sender": r["sender"],
            "message": r["message"],
            "timestamp": str(r["timestamp"])
        }
        for r in rows
    ]

# 2. Session operations
def create_session_if_not_exists(session_id):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if session exists
    cursor.execute(f"SELECT session_id FROM sessions WHERE session_id = {placeholder}", (session_id,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(
            f"INSERT INTO sessions (session_id, summary, metadata) VALUES ({placeholder}, {placeholder}, {placeholder})",
            (session_id, "New Session created", "{}")
        )
        conn.commit()
    conn.close()

def update_session_summary(session_id, summary):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE sessions SET summary = {placeholder} WHERE session_id = {placeholder}",
        (summary, session_id)
    )
    conn.commit()
    conn.close()

# 3. Agent Execution Logging
def log_agent_execution(session_id, agent_id, logs, runtime, status, tools_list):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO agent_executions (session_id, agent_id, execution_logs, runtime, status, selected_tools) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
        (session_id, agent_id, logs, runtime, status, ",".join(tools_list))
    )
    conn.commit()
    conn.close()

# 4. Supervisor Decision Logging
def log_supervisor_decision(session_id, intent, selected_agents, reasoning, token_usage):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO supervisor_decisions (session_id, intent, selected_agents, reasoning, token_usage) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
        (session_id, intent, ",".join(selected_agents), reasoning, token_usage)
    )
    conn.commit()
    conn.close()

# 5. Short Term / Working Memory
def get_working_memory(session_id):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT context FROM short_term_memory WHERE session_id = {placeholder}", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return row["context"] if row else "{}"

def save_working_memory(session_id, context):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQLite upsert vs Postgres upsert fallback
    cursor.execute(f"SELECT id FROM short_term_memory WHERE session_id = {placeholder}", (session_id,))
    exists = cursor.fetchone()
    
    if exists:
        cursor.execute(
            f"UPDATE short_term_memory SET context = {placeholder} WHERE session_id = {placeholder}",
            (context, session_id)
        )
    else:
        cursor.execute(
            f"INSERT INTO short_term_memory (session_id, context) VALUES ({placeholder}, {placeholder})",
            (session_id, context)
        )
    conn.commit()
    conn.close()

# 6. Tasks
def get_all_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_desc, is_completed, schedule FROM tasks ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r["id"],
            "task_desc": r["task_desc"],
            "is_completed": bool(r["is_completed"]),
            "schedule": r["schedule"]
        }
        for r in rows
    ]

def save_task(task_desc, is_completed, schedule=""):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO tasks (task_desc, is_completed, schedule) VALUES ({placeholder}, {placeholder}, {placeholder})",
        (task_desc, 1 if is_completed else 0, schedule)
    )
    conn.commit()
    conn.close()

# 7. Cache operations
def get_cache_entry(cache_key):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT content, expiration FROM cache_metadata WHERE cache_key = {placeholder} AND invalidation_status = 0",
        (cache_key,)
    )
    row = cursor.fetchone()
    conn.close()
    return row if row else None

def set_cache_entry(cache_key, source, content, expiration_timestamp):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"DELETE FROM cache_metadata WHERE cache_key = {placeholder}", (cache_key,))
    cursor.execute(
        f"INSERT INTO cache_metadata (cache_key, source, content, expiration) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
        (cache_key, source, content, expiration_timestamp)
    )
    conn.commit()
    conn.close()

# 8. Calendar operations
def get_all_calendar_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, start_time, end_time FROM calendar_events ORDER BY start_time ASC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r["id"],
            "title": r["title"],
            "description": r["description"],
            "start_time": str(r["start_time"]),
            "end_time": str(r["end_time"])
        }
        for r in rows
    ]

def save_calendar_event(title, description, start_time, end_time):
    is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    placeholder = "%s" if is_postgres else "?"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO calendar_events (title, description, start_time, end_time) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
        (title, description, start_time, end_time)
    )
    conn.commit()
    conn.close()

# Initialize tables immediately on module import
try:
    init_db()
except Exception as e:
    print(f"Warning: Database initialization failed: {e}. Check if PostgreSQL is running.")
