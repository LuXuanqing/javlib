import click
from jav import app, db
from jav.models import Av, AccessLog, Status
from datetime import datetime


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Av': Av,
        'av': Av.query.first(),
        'Status': Status,
        'kvs': {
            'title': 'jojo的奇妙冒险',
            'casts': ['jojo', 'kira']
        }
    }


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
        click.echo('Drop tables')
    db.create_all()
    click.echo('Initialized database')


@app.cli.command()
def forge():
    """Generate fake messages."""
    db.drop_all()
    db.create_all()
    click.echo('Working...')
    av1 = Av(
        id='WANZ-801',
        title='オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう',
        genres=["中出", "单体作品", "姐姐", "巨乳", "女上位", "屁股"],
        casts=["篠田ゆう"],
        imgs=[
            {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-1.jpg",
             "thumb": "https://pics.javcdn.pw/sample/6r4g_1.jpg",
             "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう - 樣品圖像 -1"},
            {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-2.jpg",
             "thumb": "https://pics.javcdn.pw/sample/6r4g_2.jpg",
             "title": "WANZ - 801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう - 樣品圖像 - 2"}
        ]
    )
    log1 = AccessLog(
        av_id='WANZ-801',
        refer='https://www.javbus.com/WANZ-801',
        ts=datetime(2019, 5, 1, 10, 15, 24, 0)
    )
    log2 = AccessLog(
        av_id='WANZ-801',
        refer='https://www.javbus.com/WANZ-801',
        ts=datetime(2019, 5, 2, 23, 35, 44, 0)
    )
    db.session.add_all([av1, log1, log2])
    db.session.commit()

    click.echo('Created av and access logs')
