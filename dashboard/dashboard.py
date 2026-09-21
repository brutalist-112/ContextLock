import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contextlock.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            source_type TEXT NOT NULL,
            source_reference TEXT,
            context TEXT,
            trust_score INTEGER DEFAULT 50,
            risk_score INTEGER DEFAULT 0,
            allowed_contexts TEXT DEFAULT '',
            allowed_actions TEXT DEFAULT 'answer_question',
            status TEXT DEFAULT 'active',
            content_hash TEXT,
            parent_memory_ids TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL,
            arguments TEXT,
            influencing_memories TEXT,
            risk_score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            root_memory_id INTEGER,
            affected_items TEXT,
            recovery_status TEXT DEFAULT 'pending',
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_memory(content, source_type, source_reference="", context="general",
                trust_score=50, risk_score=0, status="active",
                allowed_contexts="", allowed_actions="answer_question",
                content_hash="", parent_memory_ids=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memories 
        (content, source_type, source_reference, context, trust_score, risk_score,
         status, allowed_contexts, allowed_actions, content_hash, parent_memory_ids, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        content, source_type, source_reference, context, trust_score, risk_score,
        status, allowed_contexts, allowed_actions, content_hash, parent_memory_ids,
        datetime.now().isoformat()
    ))
    memory_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return memory_id

def get_all_memories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memories ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_active_memories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memories WHERE status = 'active' ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_quarantined_memories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memories WHERE status = 'quarantined' ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_memory_status(memory_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE memories SET status = ? WHERE id = ?", (new_status, memory_id))
    conn.commit()
    conn.close()

def delete_memory(memory_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
    conn.commit()
    conn.close()

def get_memory_counts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM memories")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM memories WHERE status = 'active'")
    active = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM memories WHERE status = 'quarantined'")
    quarantined = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM memories WHERE status = 'pending_approval'")
    pending = cursor.fetchone()[0]
    conn.close()
    return {"total": total, "active": active, "quarantined": quarantined, "pending": pending}