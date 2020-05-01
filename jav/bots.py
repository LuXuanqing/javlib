import requests
from bs4 import BeautifulSoup
from jav.log import create_logger
from jav.config import BotConfig

logger = create_logger(__name__)


def get_html(url):
    try:
        r = requests.get(url, timeout=BotConfig.timeout, proxies=BotConfig.proxy if BotConfig.enable_proxy else {})
        logger.info('got {}'.format(url))
        return r.text
    except Exception as e:
        logger.warning(e)
        return ''


def get_imgs_from_javbus(avid, domain_url=BotConfig.domain_url):
    url = '{}/{}'.format(domain_url, avid)
    html = get_html(url)
    # 没有得到页面html内容就跳出
    if not html:
        return []
    soup = BeautifulSoup(html, 'html5lib')
    # 预览图的DOM结构：<a class="sample-box" href=full><div><img src=thumb></div></a>
    samples = soup.find_all(class_='sample-box')
    # 没有预览图就跳出
    if not samples:
        logger.warning('{} has no preview imgs'.format(avid))
        return []
    imgs = [{
        'full': sample['href'],
        'thumb': sample.find('img')['src'],
        'title': sample.find('img')['title']
    } for sample in samples]
    return imgs
