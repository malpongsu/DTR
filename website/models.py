import re
import sqlite3
from datetime import datetime

from flask import current_app, g


def normalize_rfid(raw_value):
    if raw_value is None:
        return ''

    value = str(raw_value).strip()
    value = value.replace('\r', '').replace('\n', '').replace('\t', '')
    value = re.sub(r'^(?:RFID\s*[:\-]?\s*|CARD\s*[:\-]?\s*|TAG\s*[:\-]?\s*)', '', value, flags=re.IGNORECASE)
    value = re.sub(r'[\s_\-]+', '', value)
    value = ''.join(ch for ch in value if ch.isalnum()).upper()
    return value


def get_db():
    if 'db' not in g:
        database = current_app.config['DATABASE']
        if database == ':memory:':
            shared_name = f'file:attendance_{id(current_app)}?mode=memory&cache=shared'
            connection = sqlite3.connect(shared_name, uri=True)
        else:
            connection = sqlite3.connect(database)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rfid_tag TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            rfid_tag TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    ''')
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()


def fetch_users():
    db = get_db()
    return db.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()


def get_user_by_id(user_id):
    db = get_db()
    return db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


def get_user_by_rfid(rfid_tag):
    db = get_db()
    normalized = normalize_rfid(rfid_tag)
    if not normalized:
        return None

    rows = db.execute('SELECT * FROM users').fetchall()
    for row in rows:
        if normalize_rfid(row['rfid_tag']) == normalized:
            return row
    return None


def create_user(name, rfid_tag):
    db = get_db()
    normalized = normalize_rfid(rfid_tag)
    if not normalized:
        raise ValueError('RFID tag is empty.')

    existing = get_user_by_rfid(normalized)
    if existing is not None:
        raise ValueError('RFID tag already exists.')

    db.execute(
        'INSERT INTO users (name, rfid_tag) VALUES (?, ?)',
        (name.strip(), normalized),
    )
    db.commit()
    return db.execute('SELECT * FROM users WHERE id = last_insert_rowid()').fetchone()


def update_user(user_id, name, rfid_tag):
    db = get_db()
    normalized = normalize_rfid(rfid_tag)
    db.execute(
        'UPDATE users SET name = ?, rfid_tag = ? WHERE id = ?',
        (name.strip(), normalized, user_id),
    )
    db.commit()


def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM attendance WHERE user_id = ?', (user_id,))
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()


def register_attendance(user_id, rfid_tag):
    db = get_db()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute(
        'INSERT INTO attendance (user_id, rfid_tag, timestamp) VALUES (?, ?, ?)',
        (user_id, rfid_tag, timestamp),
    )
    db.commit()
    return {'timestamp': timestamp}


def has_attendance_today(user_id):
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    row = db.execute(
        "SELECT 1 FROM attendance WHERE user_id = ? AND substr(timestamp, 1, 10) = ? LIMIT 1",
        (user_id, today),
    ).fetchone()
    return row is not None


def get_recent_attendance(limit=10):
    db = get_db()
    query = '''
        SELECT a.id, u.name, a.rfid_tag, a.timestamp
        FROM attendance a
        INNER JOIN users u ON u.id = a.user_id
        ORDER BY a.id DESC
        LIMIT ?
    '''
    return db.execute(query, (limit,)).fetchall()


def get_monthly_attendance_summary():
    db = get_db()
    rows = db.execute(
        '''
        SELECT strftime('%Y-%m', timestamp) AS month,
               COUNT(*) AS total
        FROM attendance
        GROUP BY strftime('%Y-%m', timestamp)
        ORDER BY month DESC
    '''
    ).fetchall()
    return rows
