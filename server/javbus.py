import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    try:
        r = requests.get(url)
        return r.text
    except Exception as err:
        print(err)
        return ''


def get_url(bango):
    base_url = 'https://www.javbus6.pw/'
    return base_url + bango


def get_pics(bango):
    url = get_url(bango)
    html = get_html(url)
    soup = BeautifulSoup(html, 'html5lib')

    # 预览图的DOM结构：<a href=full><div><img src=thumb></div></a>
    # 预览图的class='sample-box'
    samples = soup.find_all(class_='sample-box')

    pics = []
    for sample in samples:
        pic = {}
        pic['full'] = sample['href']
        pic['thumb'] = sample.find('img')['src']
        pic['title'] = sample.find('img')['title']
        pics.append(pic)
    return json.dumps(pics)


if __name__ == '__main__':
    print(get_pics('MIDE-535'))
    print(get_pics('KDKJ-065'))