import os
import sqlite3
from typing import List, Tuple

DB_PATH = "assistant.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT UNIQUE
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            filename TEXT,
            text TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        )"""
    )
    conn.commit()
    conn.close()


def get_case_id(client_name: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM cases WHERE client_name=?", (client_name,))
    row = c.fetchone()
    if row:
        case_id = row[0]
    else:
        c.execute("INSERT INTO cases(client_name) VALUES(?)", (client_name,))
        case_id = c.lastrowid
        conn.commit()
    conn.close()
    return case_id


def add_document(case_id: int, filename: str, text: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO documents(case_id, filename, text) VALUES(?,?,?)",
        (case_id, filename, text),
    )
    conn.commit()
    conn.close()


def list_documents(case_id: int) -> List[Tuple[int, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, filename FROM documents WHERE case_id=?", (case_id,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_document_text(doc_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT text FROM documents WHERE id=?", (doc_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""
