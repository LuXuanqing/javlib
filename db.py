import sqlite3
import json
import time

DBPATH = '/Users/luxuanqing/FE/javlib/jav.db'

'''
schema
id: String, 番号，形如EKDV-413
imgs: Text, 图片的信息的json string
casts: String, 演员信息的json string
genres: String, 类型的json string
last_updated: DateTime, 上次修改时间，最好做到每次获取图片\不感兴趣 时自动更新
last_visited_url: String, 上次访问的网址
is_disliked: Boolean, 是否不感兴趣
need_hd

'''
# 检查该番号是否存在于数据库中
def exist(id):
    with sqlite3.connect(DBPATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM movies WHERE id=?', (id, ))
        if c.fetchone():
            return True
        else:
            return False


def insert_movie(id):
    with sqlite3.connect(DBPATH) as conn:
        c = conn.cursor()
        try:
            c.execute('INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (id, None, None, None, None, None, None))
            print('{} inserted'.format(id))
        except sqlite3.IntegrityError as err:
            print(err)
            print('{} already exists'.format(id))


def getone(id, field):
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
    with sqlite3.connect(DBPATH) as conn:
        c = conn.cursor()
        c.execute('SELECT {} FROM movies WHERE id=?'.format(field), (id, ))
        try:
            s = c.fetchone()[0]
        except TypeError:
            print("{} doesn't exist in movies table".format(id))
            return -2
        if s:
            return json.loads(s)
        else:
            return None


def setone(id, field, value):
    with sqlite3.connect(DBPATH) as conn:
        c = conn.cursor()
        s = json.dumps(value, ensure_ascii=False)
        c.execute('UPDATE movies SET {}=? WHERE id=?'.format(field), (s, id))
        print('the {} of {} has been updated'.format(field, id))


def insert_log(id, domain):
    with sqlite3.connect(DBPATH) as conn:
        c = conn.cursor()
        now = time.time()
        c.execute('INSERT INTO access_log VALUES (?, ?, ?)', (now, id, domain))
        print('{}({}) is visited at {}'.format(id, domain, now))


def get_log(id):
    with sqlite3.connect(DBPATH) as conn:
        c = conn.cursor()
        c.execute('SELECT time, domain FROM access_log WHERE id=? ORDER BY time DESC',
                  (id, ))
        return c.fetchone()
        # try:
        #     timestamp, domain = c.fetchone()
        #     return timestamp, domain
        # except TypeError as err:
        #     print(err)
        #     print("{} doesn't exist in movies table".format(id))
        #     return -2


if __name__ == '__main__':
    # ids = ['TEST-001', 'TEST-002', 'TEST-003', 'TEST-404']
    # for id in ids:
    print(get_log('ATID-298'))