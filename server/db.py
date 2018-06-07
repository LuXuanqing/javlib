import sqlite3
import json
import time

dbpath = '/Users/luxuanqing/FE/javlib/server/jav.db'

# APIs of access log
def insert_log(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        now = time.time()
        c.execute('INSERT INTO access_log VALUES (?, ?)',
                  (now, id))
        print('{}: {}'.format(id, now))


def get_last_visit(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        c.execute('SELECT time FROM access_log WHERE id=? ORDER BY time DESC',
                  (id, ))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            return None

# APIs of preview
def is_exist(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM movies WHERE id=?', (id, ))
        if c.fetchone():
            return True
        else:
            return False


def get_preview(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        c.execute('SELECT id,preview FROM movies WHERE id=?', (id, ))
        _, preview = c.fetchone()
        if preview:
            return json.loads(preview)
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
        c.execute('UPDATE movies SET preview=? WHERE id=?', (preview_str, id))


# APIs of info
def has_info(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        c.execute('SELECT genres,"cast" FROM movies WHERE id=?', (id, ))
        genres, cast = c.fetchone()
        has_genres = genres is not None
        has_cast = cast is not None
        return has_cast or has_genres


def update_info(id, genres, cast):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        genres_str = json.dumps(genres)
        cast_str = json.dumps(cast)
        c.execute('UPDATE movies SET genres=?, "cast"=? WHERE id=?',
                  (genres_str, cast_str, id))


if __name__ == '__main__':
    print(get_last_time('TEST-001'))
