import os
import re
import sqlite3
from datetime import datetime

from flask import current_app, g

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:  # pragma: no cover - optional dependency for hosted Postgres
    psycopg2 = None
    RealDictCursor = None


def normalize_rfid(raw_value):
    if raw_value is None:
        return ''

    value = str(raw_value).strip()
    value = value.replace('\r', '').replace('\n', '').replace('\t', '')
    value = re.sub(r'^(?:RFID\s*[:\-]?\s*|CARD\s*[:\-]?\s*|TAG\s*[:\-]?\s*)', '', value, flags=re.IGNORECASE)
    value = re.sub(r'[\s_\-]+', '', value)
    value = ''.join(ch for ch in value if ch.isalnum()).upper()
    return value


def is_postgres_database(database_url):
    return isinstance(database_url, str) and database_url.startswith(('postgresql://', 'postgres://'))


def require_postgres_driver():
    if psycopg2 is None:
        raise RuntimeError('psycopg2 is required for PostgreSQL databases. Install it with: pip install psycopg2-binary')


def get_db():
    if 'db' not in g:
        database = current_app.config['DATABASE']
        if is_postgres_database(database):
            require_postgres_driver()
            connection = psycopg2.connect(database)
            connection.cursor_factory = RealDictCursor
        elif database == ':memory:':
            shared_name = f'file:attendance_{id(current_app)}?mode=memory&cache=shared'
            connection = sqlite3.connect(shared_name, uri=True)
        else:
            db_dir = os.path.dirname(database)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            connection = sqlite3.connect(database)
        connection.row_factory = getattr(connection, 'row_factory', None) or sqlite3.Row
        g.db = connection
    return g.db


def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def _db_placeholder():
    return '%s' if is_postgres_database(current_app.config['DATABASE']) else '?'


def _execute_write(query, params=()):
    db = get_db()
    if is_postgres_database(current_app.config['DATABASE']):
        with db.cursor() as cursor:
            cursor.execute(query, params)
        db.commit()
        return None
    db.execute(query, params)
    db.commit()


def _execute_read(query, params=(), fetch='all'):
    db = get_db()
    if is_postgres_database(current_app.config['DATABASE']):
        with db.cursor() as cursor:
            cursor.execute(query, params)
            if fetch == 'one':
                return cursor.fetchone()
            return cursor.fetchall()
    cursor = db.execute(query, params)
    if fetch == 'one':
        return cursor.fetchone()
    return cursor.fetchall()


def init_db():
    db = get_db()
    if is_postgres_database(current_app.config['DATABASE']):
        with db.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    rfid_tag TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    rfid_tag TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
        db.commit()
        return

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
    return _execute_read('SELECT * FROM users ORDER BY created_at DESC')


def get_user_by_id(user_id):
    return _execute_read('SELECT * FROM users WHERE id = %s', (user_id,), fetch='one') if is_postgres_database(current_app.config['DATABASE']) else get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


def get_user_by_rfid(rfid_tag):
    normalized = normalize_rfid(rfid_tag)
    if not normalized:
        return None

    rows = _execute_read('SELECT * FROM users')
    for row in rows:
        if normalize_rfid(row['rfid_tag']) == normalized:
            return row
    return None


def create_user(name, rfid_tag):
    normalized = normalize_rfid(rfid_tag)
    if not normalized:
        raise ValueError('RFID tag is empty.')

    existing = get_user_by_rfid(normalized)
    if existing is not None:
        raise ValueError('RFID tag already exists.')

    placeholder = _db_placeholder()
    query = f'INSERT INTO users (name, rfid_tag) VALUES ({placeholder}, {placeholder})'
    _execute_write(query, (name.strip(), normalized))

    if is_postgres_database(current_app.config['DATABASE']):
        return _execute_read('SELECT * FROM users ORDER BY id DESC LIMIT 1', fetch='one')
    return get_db().execute('SELECT * FROM users WHERE id = last_insert_rowid()').fetchone()


def update_user(user_id, name, rfid_tag):
    normalized = normalize_rfid(rfid_tag)
    placeholder = _db_placeholder()
    query = f'UPDATE users SET name = {placeholder}, rfid_tag = {placeholder} WHERE id = {placeholder}'
    _execute_write(query, (name.strip(), normalized, user_id))


def delete_user(user_id):
    _execute_write('DELETE FROM attendance WHERE user_id = %s', (user_id,)) if is_postgres_database(current_app.config['DATABASE']) else _execute_write('DELETE FROM attendance WHERE user_id = ?', (user_id,))
    _execute_write('DELETE FROM users WHERE id = %s', (user_id,)) if is_postgres_database(current_app.config['DATABASE']) else _execute_write('DELETE FROM users WHERE id = ?', (user_id,))


def register_attendance(user_id, rfid_tag):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    placeholder = _db_placeholder()
    query = f'INSERT INTO attendance (user_id, rfid_tag, timestamp) VALUES ({placeholder}, {placeholder}, {placeholder})'
    _execute_write(query, (user_id, rfid_tag, timestamp))
    return {'timestamp': timestamp}


def has_attendance_today(user_id):
    today = datetime.now().strftime('%Y-%m-%d')
    if is_postgres_database(current_app.config['DATABASE']):
        row = _execute_read(
            'SELECT 1 FROM attendance WHERE user_id = %s AND DATE(timestamp) = %s LIMIT 1',
            (user_id, today),
            fetch='one',
        )
    else:
        row = get_db().execute(
            "SELECT 1 FROM attendance WHERE user_id = ? AND substr(timestamp, 1, 10) = ? LIMIT 1",
            (user_id, today),
        ).fetchone()
    return row is not None


def get_recent_attendance(limit=10):
    return _execute_read(
        '''
        SELECT a.id, u.name, a.rfid_tag, a.timestamp
        FROM attendance a
        INNER JOIN users u ON u.id = a.user_id
        ORDER BY a.id DESC
        LIMIT %s
        ''',
        (limit,),
    ) if is_postgres_database(current_app.config['DATABASE']) else get_db().execute(
        '''
        SELECT a.id, u.name, a.rfid_tag, a.timestamp
        FROM attendance a
        INNER JOIN users u ON u.id = a.user_id
        ORDER BY a.id DESC
        LIMIT ?
        ''',
        (limit,),
    ).fetchall()


def get_monthly_attendance_summary():
    if is_postgres_database(current_app.config['DATABASE']):
        return _execute_read(
            '''
            SELECT TO_CHAR(timestamp::timestamp, 'YYYY-MM') AS month,
                   COUNT(*) AS total
            FROM attendance
            GROUP BY TO_CHAR(timestamp::timestamp, 'YYYY-MM')
            ORDER BY month DESC
            '''
        )

    return get_db().execute(
        '''
        SELECT strftime('%Y-%m', timestamp) AS month,
               COUNT(*) AS total
        FROM attendance
        GROUP BY strftime('%Y-%m', timestamp)
        ORDER BY month DESC
    '''
    ).fetchall()
