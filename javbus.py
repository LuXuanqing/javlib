import requests
from bs4 import BeautifulSoup
# create and configure logger
import logging
logging.basicConfig(filename='test.log',
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s,%(name)s,%(levelname)s,%(message)s')
logger = logging.getLogger(__name__)

BASE_URL = 'https://www.javbus.com/'
HEADERS = {
    'accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':
    'gzip, deflate, br',
    'accept-language':
    'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
    'referer':
    'https://www.javbus.com/',
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}
PROXIES = {
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087',
}


def get_html(url):
    try:
        r = requests.get(url, timeout=5, proxies=PROXIES)
        logger.info('got html')
        return r.text
    except Exception as err:
        logger.error('failed to get html')
        return ''


def get_previews(id):
    url = BASE_URL + id
    html = get_html(url)
    # 没有得到页面html内容就跳出
    if not html:
        return None
    soup = BeautifulSoup(html, 'html5lib')
    # 预览图的DOM结构：<a class="sample-box" href=full><div><img src=thumb></div></a>
    samples = soup.find_all(class_='sample-box')
    # 没有预览图就跳出
    if not samples:
        return None
    previews = []
    for sample in samples:
        p = {
            'full': sample['href'],
            'thumb': sample.find('img')['src'],
            'title': sample.find('img')['title']
        }
        previews.append(p)
    return previews


if __name__ == '__main__':
    print(get_previews('LKD-004'))
    print(get_previews('MILK-039'))
    # print(get_html('https://www.javbus.com/LKD-004'))
