import os
import sys
import pymongo
from threading import Thread
import queue
import requests as rs
import re
from bs4 import BeautifulSoup as bs
import time


class UrlResponError(OSError):
    pass


class CONFIG:
    """
    class CONFIG
    """
    TOTAL_PAGES = 21
    ROOT_DOMAIN = r'https://www.51voa.com'
    SUB_URL = r'/VOA_Special_English/'
    MASTR_URL = r'https://www.51voa.com/This_is_America_{}.html'
    HEAD = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 '
        'Safari/537.36 '
    }
    URL_QUEUE = queue.Queue()
    MP3_QUEUE = queue.Queue()
    MESSAGE_QUEUE = queue.Queue()
    START_TIME = time.time()
    SPIDER_NUM = 10
    COMPLETE_LIST = [i for i in range(0, TOTAL_PAGES + 1)]
    COMPLETE_MP3 = [[0 for __ in range(50)]] + [[1 for __ in range(50)]
                                                for _ in range(0, TOTAL_PAGES)]

    @staticmethod
    def refresh_status():
        """
        目标数据爬取状态刷新
        """
        with CONFIG.LOCK:
            for i in range(len(CONFIG.COMPLETE_MP3)):
                if sum(CONFIG.COMPLETE_MP3[i]) == 0:
                    CONFIG.COMPLETE_LIST[i] = 0
        pass

    @staticmethod
    def get_html(url):
        """
        获取目标网页 html 源码
        :param url: 要访问的网站 url
        :return: 基于 requests 库的返回结果
        """
        # url = re.sub(r'\.[0-9a-zA-z]*\.com', '.51voa.com', url)
        for i in range(11):
            try:
                r = rs.get(url, headers=CONFIG.HEAD)
                if r.status_code == 200:
                    return r
            except rs.exceptions.ProxyError:
                continue
            if i == 10:
                raise UrlResponError(
                    'Unable to get an effective response from {}! {}'.format(
                        url, r))

    @staticmethod
    def send_message(message):
        '''
        向信息队列中发送信息。 该队列仅供传输控制台信息使用
        :param message: 要发送的信息
        :return: None
        '''
        CONFIG.MESSAGE_QUEUE.put(message)
        pass

    @staticmethod
    def receive_message():
        '''
        从信息队列中接受信息。 该队列仅供传输控制台信息使用
        :return: None
        '''
        return CONFIG.MESSAGE_QUEUE.get()


class MainPageSpider(Thread):
    '''
    class MainPageSpider, a subclass for Thread.
    '''
    def __init__(self):
        super().__init__()
        self.curnum = None
        pass

    def get_url_list(self):
        '''
        获取主目录下各个文章的 url 列表
        :return: 各个文章的 url （以字典形式存放）
        '''
        r = CONFIG.get_html(CONFIG.MASTR_URL.format(self.curnum))
        r.encoding = 'utf-8'
        soup = bs(r.content, 'lxml')
        sub_url = soup.find('div', class_='List')
        urls = sub_url.find_all('li')
        urls_dict = {}
        for i in urls:
            temptitle = ' '.join(i.text.split())
            temptitle = re.sub(r'[\/:*?"<>|]', '_', temptitle)
            urls_dict[temptitle] = CONFIG.ROOT_DOMAIN + i.a.get('href')
        return urls_dict

    def send_urls_dict(self, urls_dict: dict):
        '''
        向 URL 队列中放入 url 字典
        :param urls_dict: 要放入的 url 字典
        :return: None
        '''
        res = {'No': self.curnum, 'urls': urls_dict}
        CONFIG.URL_QUEUE.put(res)
        pass

    def send_none(self):
        '''
        向 URL 队列中放入 None
        :return: None
        '''
        for _ in range(CONFIG.SPIDER_NUM):
            CONFIG.URL_QUEUE.put(None)

    def run(self):
        for i in CONFIG.COMPLETE_LIST:
            if i != 0:
                self.curnum = i
            else:
                continue
            res = self.get_url_list()
            self.send_urls_dict(res)
        self.send_none()
        pass


# TODO page info
class ArticleSpider(Thread):
    '''
    class ArticleSpider, a subclass for Thread.
    '''
    def __init__(self):
        super().__init__()
        self.r = None
        self.curnum = None
        self.curmp3num = -1
        self.curdict = None
        self.curtitle = None
        self.cururl = None
        self.curpageinfo = None
        pass

    def get_urls_dict(self):
        '''
        从 url 队列中获取 url 字典
        :return: 1 for success, None for failed
        '''
        urls_dict = CONFIG.URL_QUEUE.get()
        if urls_dict is None:
            return None
        else:
            self.curnum = urls_dict['No']
            self.curdict = urls_dict['urls']
            return 1

    def get_url(self):
        '''
        获取要爬取的文章的 html 源码
        :return: None
        '''
        self.r = CONFIG.get_html(self.cururl)
        pass

    def get_page_info(self):
        '''
        获取要爬取的文章的内容
        :return: None
        '''
        r = self.r
        self.curpageinfo = {}
        r.encoding = 'utf-8'
        soup = bs(r.content, 'lxml')
        article = soup.find('div', class_='Content')
        author = article.find('span', class_='byline')
        datetime = article.find('span', class_='datetime')
        res = []
        mp3_url = soup.find('div', class_='menubar')
        try:  # 尝试获取MP3url
            mp3url = mp3_url.find('a', id='mp3').get('href')
        except AttributeError:
            mp3url = None
        if author is None:  # 确定网页中是否有创作者信息
            pass
        else:
            res.append(author.text)
        if datetime is None:  # 确定网页中是否有日期信息
            pass
        else:
            res.append(datetime.text)
        for i in article.find_all('p'):
            res.append(' '.join(i.text.split()))
        pass

    def send_page_info(self):
        '''
        将 mp3 信息放入 mp3 队列
        :return: None
        '''
        CONFIG.MP3_QUEUE.put(self.curpageinfo)
        pass

    def send_none(self):
        '''
        将 None 放入 MP3 队列
        :return: None
        '''
        for _ in range(CONFIG.SPIDER_NUM):
            CONFIG.MP3_QUEUE.put(None)

    def run(self):
        while True:
            urls_dict = self.get_urls_dict()
            if urls_dict is None:
                break
            else:
                self.curmp3num = -1
                for self.curtitle, self.cururl in self.curdict.items():
                    self.curmp3num += 1
                    self.get_url()
                    self.get_page_info()
                    self.send_page_info()
        self.send_none()
        pass


class VOADataBase(Thread):
    """
    class VOADataBase, a subclass for Thread.
    """
    def __init__(self):
        super().__init__()
        pass

    def get_page_info(self):
        pass

    def write_page_info(self):
        pass

    def run(self):
        pass


class SpiderMonitor:
    '''
    class SpiderMonitor, a subclass for Thread.
    '''
    def __init__(self):
        super().__init__()
        self.num_of_files = 0
        self.cnt_num = 0
        self.cnt_mem = 0
        self.run_time = 0
        self.remain_time = 0
        self.remain_mem = 0
        self.nonecnt = 0
        pass

    def cnf(self):
        '''
        cnf stand for caculate number of files
        :return: None
        '''
        flag = 0
        for i in CONFIG.COMPLETE_LIST:
            if i != 0:
                flag += 1
        self.num_of_files = flag * 50
        pass

    def cot(self):
        '''
        cot stand for continuous operation time
        :return: None
        '''
        self.run_time = time.time() - CONFIG.START_TIME
        pass

    def etc(self):
        '''
        etc stand for estimated time of completion
        :return: None
        '''
        temp = self.num_of_files * self.run_time / self.cnt_num
        self.remain_time = temp - self.run_time
        pass

    def emc(self):
        '''
        emc stand for estimated memory of completion
        :return: None
        '''
        temp = self.num_of_files * self.cnt_mem / self.cnt_num
        self.remain_mem = temp - self.cnt_mem
        pass

    def get_state(self):
        '''
        获取当前爬虫进度状态。
        :return: None for break, 0 for continue, -1 for succeed
        '''
        message = CONFIG.receive_message()
        if message is None:
            self.nonecnt += 1
            if self.nonecnt == CONFIG.SPIDER_NUM:
                return None
            return 0
        self.cnt_num += 1
        self.cnt_mem += message
        self.cot()
        self.etc()
        self.emc()
        return -1

    def run(self):
        self.cnf()
        while True:
            flag = self.get_state()
            os.system('cls')
            stat = '''Run Time : {} s\nSpider Rate : {}/{}\nMemory Usaged : {} MB\nRemain Time : {} s, Remain Menory 
            : {} MB\nNumer of Running Spiders : {}'''.format(
                self.run_time, self.cnt_num, self.num_of_files,
                self.cnt_mem / (1024 * 1024), self.remain_time,
                self.remain_mem / (1024 * 1024),
                CONFIG.SPIDER_NUM - self.nonecnt)
            print(stat)
            if flag is None:
                print('Complete')
                break


class Master:
    '''
    class Master
    '''
    def __init__(self):
        self.MPS = None
        self.AS_list = []
        self.MS_list = []
        self.SM = None
        self.SR = None
        pass

    def _creat_MPS(self):
        self.MPS = MainPageSpider()
        self.MPS.start()
        pass

    def _creat_AS(self):
        for _ in range(CONFIG.SPIDER_NUM):
            self.AS_list.append(ArticleSpider())
        for i in self.AS_list:
            i.start()
        pass

    def _creat_MS(self):
        for _ in range(CONFIG.SPIDER_NUM):
            self.MS_list.append(MP3Spider())
        for i in self.MS_list:
            i.start()
        pass

    def _creat_SM(self):
        self.SM = SpiderMonitor()
        self.SM.start()
        pass

    def _creat_SR(self):
        self.SR = SpiderRecovery()
        self.SR.start()
        pass

    def creat_all(self):
        '''
        创建各个线程并启动
        :return: None
        '''
        self._creat_MPS()
        self._creat_AS()
        self._creat_MS()
        self._creat_SM()
        self._creat_SR()
        pass

    def join_all(self):
        '''
        阻塞 Master 线程，等待所有线程结束后再继续
        :return: None
        '''
        self.MPS.join()
        for i in self.AS_list:
            i.join()
        for i in self.MS_list:
            i.join()
        self.SM.join()
        self.SR.join()
        pass

    def run(self):
        SpiderRecovery.recovery()
        self.creat_all()
        self.join_all()
        print('Finish')
        pass


def main():
    t = Master()
    t.run()
    pass


if __name__ == '__main__':
    main()
    pass
