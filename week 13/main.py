import os
import sys
import requests as rs
import re
from bs4 import BeautifulSoup as bs
import time
from faker import Faker
from threading import Thread


class UrlResponError(OSError):
    pass


class CONFIG:
    '''
    '''
    ROOT_DOMAIN = r'https://www.51voa.com'
    MASTR_URL = r'https://www.51voa.com/VOA_Standard_{}.html'
    HEAD = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }


class MainPageSpider(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        pass


class MP3Spider(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        pass


class ArticleSpyder(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        pass


class SpyderMonitor(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        pass


class Master:
    '''
    '''
    def __init__(self):
        pass


def get_url_list(master_url_index):
    '''
    '''
    r = rs.get(CONFIG.MASTR_URL.format(master_url_index), headers=CONFIG.HEAD)
    r.encoding = 'utf-8'
    soup = bs(r, 'lxml')
    sub_url = soup.find('div', class_='List')
    urls = sub_url.find_all('li')
    urls_dict = {}
    for i in urls:
        urls_dict[' '.join(
            i.text.split())] = CONFIG.ROOT_DOMAIN + i.a.get('href')
    return urls_dict


def get_mp3_info(url):
    '''
    '''
    r = rs.get(url, headers=CONFIG.HEAD)
    r.encoding = 'utf-8'
    soup = bs(r, 'lxml')
    mp3_url = soup.find('div', class_='menubar')
    mp3_info_dict = {
        'mp3':
        mp3_url.find('a', id='mp3').get('href'),
        'lrc':
        CONFIG.ROOT_DOMAIN + mp3_url.find('a', id='lrc').get('href'),
        'translate':
        CONFIG.ROOT_DOMAIN + r'/VOA_Standard_English/' +
        mp3_url.find('a', id='EnPage').get('href')
    }
    return mp3_info_dict


def get_music(url, save_to):
    '''
    '''
    r = rs.get(url, headers=CONFIG.HEAD)
    r.encoding = 'utf-8'
    with open(save_to, 'w', encoding='utf-8') as f:
        f.write(r.content)
        f.flush()
    pass


def get_lrc(url, save_to):
    '''
    '''
    r = rs.get(url, headers=CONFIG.HEAD)
    r.encoding = 'utf-8'
    with open(save_to, 'w', encoding='utf-8') as f:
        f.write(r.content)
        f.flush()
    pass


def get_article(url, save_to):
    '''
    '''
    r = rs.get(url, headers=CONFIG.HEAD)
    r.encoding = 'utf-8'
    soup = bs(r, 'lxml')
    article = soup.find('div', class_='Content')
    res = []
    for i in article.find_all('p'):
        res.append(' '.join(i.text.split()))
    with open(save_to, 'w', encoding='utf-8') as f:
        for i in res:
            f.write(i)
            f.write('\n')
        f.flush()
    pass


def get_translate(url, save_to):
    '''
    '''
    r = rs.get(url, headers=CONFIG.HEAD)
    r.encoding = 'utf-8'
    soup = bs(r, 'lxml')
    article = soup.find('div', class_='Content')
    res = []
    for i in article.find_all('p'):
        res.append(' '.join(i.text.split()))
    with open(save_to, 'w', encoding='utf-8') as f:
        for i in res:
            f.write(i)
            f.write('\n')
        f.flush()
    pass


def main():
    pass


if __name__ == '__main__':
    main()
    pass
