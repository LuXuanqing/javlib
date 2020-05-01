import unittest
from jav.bots import get_html, get_imgs_from_javbus
from jav import app, db
from jav.models import Av, AccessLog
from jav.commands import initdb, forge, make_shell_context
from jav.log import create_logger

logger = create_logger(__name__)


class CommandsTestCase(unittest.TestCase):
    def setUp(self):  # 更新配置
        app.config.update(TESTING=True,
                          SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        # 创建数据库和表
        db.create_all()
        # 创建测试数据
        av_id = 'TEST-001'
        av = Av(id=av_id)
        log = AccessLog(av_id=av_id)
        db.session.add_all([av, log])
        db.session.commit()
        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表

    def test_initdb(self):
        # without --drop
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database', result.output)
        # with --drop
        result = self.runner.invoke(initdb, '--drop')
        self.assertIn('Initialized database', result.output)
        self.assertIn('Drop tables', result.output)

    def test_forge(self):
        result = self.runner.invoke(forge)
        self.assertIn('Working...', result.output)
        self.assertNotEqual(Av.query.count(), 0)
        self.assertNotEqual(AccessLog.query.count(), 0)
        self.assertIn('Created av and access logs', result.output)

    def test_make_shell_context(self):
        # 很水，没什么用，就是为了凑覆盖率
        rv = make_shell_context()
        self.assertIn('av', rv)


class BaseModelTestCase(unittest.TestCase):
    def setUp(self):
        # 更新配置
        app.config.update(TESTING=True,
                          SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        # 创建数据库和表
        db.create_all()

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表

    # 测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])


class AccessLogModelTestCase(BaseModelTestCase):
    def test_create(self):
        # 测试创建
        log = AccessLog(av_id='TEST-001', refer='www.javbus.com')
        log.save()
        self.assertGreater(AccessLog.query.count(), 0)

    def test_repr(self):
        log = AccessLog(av_id='TEST-001', refer='www.javbus.com')
        log.save()
        repr = log.__repr__()
        self.assertIn('TEST-001', repr)
        self.assertIn('javbus', repr)

    def test_refer_site(self):
        log1 = AccessLog(av_id='TEST-001', refer='www.javbus.com')
        log2 = AccessLog(av_id='TEST-001', refer='www.javlib.com')
        log3 = AccessLog(av_id='TEST-001', refer='www.pornhub.com')
        log4 = AccessLog(av_id='TEST-001')
        self.assertEqual(log1.refer_site, 'javbus')
        self.assertEqual(log2.refer_site, 'javlib')
        self.assertEqual(log3.refer_site, 'other')
        self.assertEqual(log4.refer_site, '')


class AvModelTestCase(BaseModelTestCase):
    def test_create_av(self):
        av = Av(id='TEST-001')
        av.save()
        self.assertGreater(Av.query.count(), 0)

    def test_repr(self):
        av = Av(id='TEST-001')
        av.save()
        self.assertIn('TEST-001', str(av))

    def test_init_attr(self):
        av = Av(id='TEST-001', title='test title')
        av.save()
        av.init_attr(**{
            'title': 'title is modified',
            'casts': ['lulu', 'huihui']
        })
        av.save()
        self.assertEqual('test title', av.title)  # 已赋值的属性不会被修改
        self.assertEqual(['lulu', 'huihui'], av.casts)

    def test_update_attr(self):
        av = Av(id='TEST-001', title='first title', status='WANTED')
        av.save()
        av.update_attr(**{
            'title': '',
            'status': 'OWNED',
            'rating': 'FAVORITE'
        })
        av.save()
        self.assertEqual('first title', av.title)  # 写入空值不生效
        self.assertEqual('OWNED', av.status.name)
        self.assertEqual('FAVORITE', av.rating.name)

    def test_save_faile(self):
        av = Av(id='TEST-001', title='first title', status='WANTED')
        av.save()
        av.update_attr(status='BAD')
        av.save()
        self.assertEqual(av.status.name, 'WANTED')

    def test_last_visit(self):
        av = Av(id='TEST-001')
        av.save()
        self.assertIsNone(av.last_visit)
        log = AccessLog(av_id='TEST-001', refer='www.javbus.com/TEST-001')
        log.save()
        self.assertIsNotNone(av.last_visit)
        import datetime
        self.assertIsInstance(av.last_visit['ts'], datetime.datetime)
        self.assertIsNotNone(av.last_visit['refer_site'])


class BotsTestCase(unittest.TestCase):
    def test_get_html(self):
        # 测试成功获得html
        data = get_html('https://www.javbus.com/WANZ-801')
        self.assertIn('WANZ-801', data)
        self.assertIn('JavBus', data)

        # 测试获取html失败
        data = get_html('https://localhost/failed/404')
        self.assertEqual(data, '')

    def test_get_imgs_from_javbus(self):
        # 测试成功获取imgs
        imgs = get_imgs_from_javbus('WANZ-801')
        self.assertGreater(len(imgs), 1)
        img = imgs[0]
        self.assertIn('full', img)
        self.assertIn('thumb', img)
        self.assertIn('title', img)

        # 打开javbus页面，但没有图片
        imgs = get_imgs_from_javbus('LUZH')
        self.assertEqual(imgs, [])

        # 没打开javbus页面
        imgs = get_imgs_from_javbus('LUZH', 'https://localhost/fail')
        self.assertEqual(imgs, [])


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        # 更新配置
        app.config.update(TESTING=True,
                          SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        # 创建数据库和表
        db.create_all()
        # 创建测试数据
        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器
        self.runner.invoke(forge)

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表

    def test_fetch_av_existed(self):
        av_id = 'WANZ-801'
        response = self.client.post('/api/av/{}'.format(av_id))
        logger.debug(dir(response))
        data = response.get_json()
        logger.debug(data)
        self.assertIn('imgs', data)
        self.assertIn('status', data)
        self.assertIn('rating', data)
        self.assertIn('last_visit', data)

    def test_fetch_av_not_existed(self):
        av_id = 'TEST-001'
        self.assertIsNone(Av.query.get(av_id))
        response = self.client.post('/api/av/{}'.format(av_id))
        data = response.get_json()
        self.assertNotIn('status', data)
        self.assertNotIn('rating', data)
        self.assertNotIn('last_visit', data)
        self.assertIsNotNone(Av.query.get(av_id))




if __name__ == '__main__':
    unittest.main()
