import requests
from bs4 import BeautifulSoup
from jav.log import create_logger

logger = create_logger(__name__)

domain_url = 'https://www.javbus.com/'
proxy = {
    'http': 'http://raspberrypi:7890',
    'https': 'http://raspberrypi:7890',
}
headers = {
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


def get_html(url):
    try:
        r = requests.get(url, timeout=10, proxies=proxy)
        return r.text
    except Exception:
        return ''


def get_previews(id):
    url = domain_url + id
    html = get_html(url)
    # 没有得到页面html内容就跳出
    if not html:
        logger.warning('Can\'t get HTML from {}'.format(id))
        return None
    soup = BeautifulSoup(html, 'html5lib')
    # 预览图的DOM结构：<a class="sample-box" href=full><div><img src=thumb></div></a>
    samples = soup.find_all(class_='sample-box')
    # 没有预览图就跳出
    if not samples:
        logger.warning('{} has no preview imgs'.format(id))
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
