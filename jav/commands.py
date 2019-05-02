import click

from jav import app, db
from jav.models import Av, History


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Av=Av, History=History)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?',
                      abort=True)
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
        genres='["中出", "单体作品", "姐姐", "巨乳", "女上位", "屁股"]',
        casts='["篠田ゆう"]',
        imgs='[{"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-1.jpg", "thumb": '
             '"https://pics.javcdn.pw/sample/6r4g_1.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう - 樣品圖像 - '
             '1"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-2.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_2.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 2"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-3.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_3.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 3"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-4.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_4.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 4"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-5.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_5.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 5"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-6.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_6.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 6"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-7.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_7.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 7"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-8.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_8.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 8"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-9.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_9.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 篠田ゆう '
             '- 樣品圖像 - 9"}, {"full": "https://pics.dmm.co.jp/digital/video/wanz00801/wanz00801jp-10.jpg", '
             '"thumb": "https://pics.javcdn.pw/sample/6r4g_10.jpg", "title": "WANZ-801 オナニー出来ない僕を義姉がねっとり腰振り優しい騎乗位 '
             '篠田ゆう - 樣品圖像 - 10"}] '
    )
    his1 = History(
        av_id='WANZ-801',
        site='https://www.javbus.com/WANZ-801'
    )
    db.session.add(av1)
    db.session.add(his1)
    db.session.commit()
    click.echo('Created av and history')
