import sqlite3
import json

dbpath = '/Users/luxuanqing/FE/javlib/server/jav.db'


def is_exist(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM movies WHERE id=?', (id,))
        if c.fetchone():
            return True
        else:
            return False

def get_preview_by_id(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        c.execute('SELECT preview FROM movies WHERE id=?', (id, ))
        value = c.fetchone()
        if value:
            return json.loads(value[0])
        else:
            return None


def insert_movie(id, preview):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        preview_str = json.dumps(preview)
        c.execute('INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (id, preview_str, None, None, None, None, None))


def update_preview(id, preview):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        preview_str = json.dumps(preview)
        c.execute('UPDATE movies SET preview=? WHERE id=?',
                  (preview_str, id))
