import sqlite3
import json
import time

dbpath = '/Users/luxuanqing/FE/javlib/server/jav.db'


class movie():
    def exist(id):
        with sqlite3.connect(dbpath) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM movies WHERE id=?', (id, ))
            if c.fetchone():
                return True
            else:
                return False

    def insert(id):
        with sqlite3.connect(dbpath) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (id, None, None, None, None, None, None))

    def fetchone(field, id):
        '''根据id取得相应field的值
        Arguments：
        field - str
        id - str
        Return：
        list: 正常
        []: 记录为"[]"(爬取的数据为空)
        None: 该字段为null
        -2: 表中没有这个id
        '''
        with sqlite3.connect(dbpath) as conn:
            c = conn.cursor()
            c.execute('SELECT {} FROM movies WHERE id=?'.format(field),
                      (id, ))
            try:
                s = c.fetchone()[0]
            except TypeError as identifier:
                print("{} doesn't exist in movies table".format(id))
                return -2
            if s:
                return json.loads(s)
            else:
                return None


    # 所有查询的默认前提是该id存在于movies表中，否则可能报错，所以查询前需要确保用exist方法检查过
    def get_preview(id):
        field = 'preview'
        return movie.fetchone(field, id)

    def set_preview(id, preview):
        with sqlite3.connect(dbpath) as conn:
            c = conn.cursor()
            preview_str = json.dumps(preview)
            c.execute('UPDATE movies SET preview=? WHERE id=?',
                      (preview_str, id))

    def has_info(id):
        with sqlite3.connect(dbpath) as conn:
            c = conn.cursor()
            c.execute('SELECT genres,"cast" FROM movies WHERE id=?', (id, ))
            genres, cast = c.fetchone()
            has_genres = genres is not None
            has_cast = cast is not None
            return has_cast or has_genres

    def get_genres(id):
        '''如果数据库没有数据(null)返回None，如果记录为'[]'(没爬到数据)返回-1
        '''
        with sqlite3.connect(dbpath) as conn:
            c = conn.cursor()
            c.execute('SELECT genres FROM movies WHERE id=?', (id, ))
            genres_str = c.fetchone()[0]


# APIs of access log
def insert_log(id):
    with sqlite3.connect(dbpath) as conn:
        c = conn.cursor()
        now = time.time()
        c.execute('INSERT INTO access_log VALUES (?, ?)', (now, id))
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
    print(movie.get_preview('TEST-001'))
    print(movie.get_preview('TEST-002'))
    print(movie.get_preview('TEST-001111'))
    print(movie.get_preview('SPYE-170'))
