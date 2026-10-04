import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        db_path = current_app.config.get("DATABASE_URL", "smartlead.db")
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = sqlite3.connect(app.config.get("DATABASE_URL", "smartlead.db"))
        db.execute(
            '''CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )'''
        )
        db.commit()
        db.close()
    app.teardown_appcontext(close_db)

def lead_ekle(isim, telefon, mesaj):
    db = get_db()
    cur = db.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj),
    )
    db.commit()
    return cur.lastrowid

def tum_leadler():
    db = get_db()
    rows = db.execute(
        "SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC"
    ).fetchall()
    return [dict(row) for row in rows]
