import os
import sys
import requests as rs
import re
from bs4 import BeautifulSoup as bs
import time
from faker import Faker
from threading import Thread
import queue


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
    URL_QUEUE = queue.Queue()
    MP3_QUEUE = queue.Queue()

    @staticmethod
    def get_html(url):
        '''
        '''
        for i in range(11):
            try:
                r = rs.get(url, headers=CONFIG.HEAD)
                if r.status_code == 200:
                    return r
            except rs.exceptions.ProxyError:
                if i == 10:
                    raise UrlResponError(
                        'Unable to get an effective response from {}!'.format(
                            url))
                else:
                    continue


class MainPageSpider(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        self.curnum = None
        pass

    def get_url_list(self):
        '''
        '''
        r = CONFIG.get_html(CONFIG.MASTR_URL.format(self.curnum))
        r.encoding = 'utf-8'
        soup = bs(r, 'lxml')
        sub_url = soup.find('div', class_='List')
        urls = sub_url.find_all('li')
        urls_dict = {}
        for i in urls:
            urls_dict[' '.join(
                i.text.split())] = CONFIG.ROOT_DOMAIN + i.a.get('href')
        return urls_dict

    def send_urls_dict(self, urls_dict: dict):
        '''
        '''
        res = {'No': self.curnum, 'urls': urls_dict}
        CONFIG.URL_QUEUE.put(res)
        pass

    def creat_folder(self):
        '''
        '''
        for i in ['mp3', 'lrc', 'article', 'translate', 'markdowm']:
            dirpath = './week 13/51voa/{}/{}'.format(self.curnum, i)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            else:
                continue
        pass

    def run(self):
        for self.curnum in range(1, 36):
            res = self.get_url_list()
            self.send_urls_dict(res)
            self.creat_folder()
        CONFIG.URL_QUEUE.put(None)
        pass


class ArticleSpider(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        self.r = None
        self.curnum = None
        self.curdict = None
        self.curtitle = None
        self.cururl = None
        pass

    def get_urls_dict(self):
        '''
        '''
        urls_dict = CONFIG.URL_QUEUE.get()
        if urls_dict is None:
            return None
        else:
            self.curnum = urls_dict['No']
            self.curnum = urls_dict['urls']
            return 1

    def get_url(self):
        '''
        '''
        self.r = CONFIG.get_html(self.cururl)
        pass

    def get_article(self, save_to):
        '''
        '''
        r = self.r
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

    def get_mp3_info(self):
        '''
        '''
        r = self.r
        r.encoding = 'utf-8'
        soup = bs(r, 'lxml')
        mp3_url = soup.find('div', class_='menubar')
        mp3_info_dict = {
            'No':
            self.curnum,
            'title':
            self.curtitle,
            'mp3':
            mp3_url.find('a', id='mp3').get('href'),
            'lrc':
            CONFIG.ROOT_DOMAIN + mp3_url.find('a', id='lrc').get('href'),
            'translate':
            CONFIG.ROOT_DOMAIN + r'/VOA_Standard_English/' +
            mp3_url.find('a', id='EnPage').get('href')
        }
        return mp3_info_dict

    def get_translate(url, save_to):
        '''
        '''
        r = CONFIG.get_html(url)
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

    def send_mp3_info(self, mp3_info_dict):
        '''
        '''
        CONFIG.MP3_QUEUE.put(mp3_info_dict)
        pass

    def run(self):
        while True:
            urls_dict = self.get_urls_dict()
            if urls_dict is None:
                break
            else:
                for self.curtitle, self.cururl in self.curdict.items():
                    self.get_url()
                    self.get_article(
                        r'./week 13/51voa/{}/article/{}.txt'.format(
                            self.curnum, self.curtitle))
                    mp3_info = self.get_mp3_info()
                    self.get_translate(
                        mp3_info['translate'],
                        r'./week 13/51voa/{}/translate/{}.txt'.format(
                            self.curnum, self.curtitle))
                    self.send_mp3_info(mp3_info)
        self.send_mp3_info(None)
        pass


class MP3Spider(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        self.curnum = None
        self.curtitle = None
        self.curmp3url = None
        self.curlrcurl = None
        pass

    def get_mp3_info(self):
        '''
        '''
        mp3_info = CONFIG.MP3_QUEUE.get()
        if mp3_info is None:
            return None
        else:
            self.curnum = mp3_info['No']
            self.curtitle = mp3_info['title']
            self.curmp3url = mp3_info['mp3']
            self.curlrcurl = mp3_info['lrc']
            return 1

    def get_music(self, save_to):
        '''
        '''
        r = CONFIG.get_html(self.curmp3url)
        r.encoding = 'utf-8'
        with open(save_to, 'w', encoding='utf-8') as f:
            f.write(r.content)
            f.flush()
        pass

    def get_lrc(self, save_to):
        '''
        '''
        r = CONFIG.get_html(self.curlrcurl)
        r.encoding = 'utf-8'
        with open(save_to, 'w', encoding='utf-8') as f:
            f.write(r.content)
            f.flush()
        pass

    def run(self):
        while True:
            res = self.get_mp3_info()
            if res is None:
                break
            else:
                self.get_music(r'./week 13/51voa/{}/mp3/{}.txt'.format(
                    self.curnum, self.curtitle))
                self.get_lrc(r'./week 13/51voa/{}/lrc/{}.txt'.format(
                    self.curnum, self.curtitle))
        pass


class SpiderMonitor(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


class SpiderRecovery(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


class Master:
    '''
    '''
    def __init__(self):
        pass

    def run(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
    pass
