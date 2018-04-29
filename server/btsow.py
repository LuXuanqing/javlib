import requests
from bs4 import BeautifulSoup

HEADERS = {
    'accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':
    'gzip, deflate, br',
    'accept-language':
    'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
    'Host':
    'btso.pw',
    'referer':
    'https://btso.pw/tags',
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}


def get_url(bangou):
    base_url = 'https://btso.pw/search/'
    return base_url + bangou


def get_html(url):
    try:
        r = requests.get(url, headers=HEADERS)
        return r.text
    except Exception as err:
        print(err)
        return ''


def get_links(bangou):
    url = get_url(bangou)
    html = get_html(url)
    soup = BeautifulSoup(html, 'html5lib')
    items = soup.select('div.data-list div[class$=row]')
    links = []
    for item in items:
        link = {}
        link['title'] = item.find('a')['title']
        link['link'] = item.find('a')['href']
        link['size'] = item.find(class_='size').text
        link['date'] = item.find(class_='date').text
        links.append(link)
    return links


if __name__ == '__main__':
    print(get_links('KAWD-889'))