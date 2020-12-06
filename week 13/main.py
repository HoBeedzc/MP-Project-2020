import os
import requests as rs
import re
from bs4 import BeautifulSoup as bs
import time
from threading import Thread, Lock
import queue


class UrlResponError(OSError):
    pass


class LogFileNotFoundError(FileNotFoundError):
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
    MESSAGE_QUEUE = queue.Queue()
    START_TIME = time.time()
    SPIDER_NUM = 5
    COMPLETE_LIST = [i for i in range(0, 36)]
    COMPLETE_MP3 = [[0 for __ in range(50)]] + [[1 for __ in range(50)]
                                                for _ in range(0, 35)]
    LOCK = Lock()

    @staticmethod
    def refresh_status():
        '''
        '''
        with CONFIG.LOCK:
            for i in range(len(CONFIG.COMPLETE_MP3)):
                if sum(CONFIG.COMPLETE_MP3[i]) == 0:
                    CONFIG.COMPLETE_LIST[i] = 0
        pass

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
                continue
            time.sleep(1)
            if i == 10:
                raise UrlResponError(
                    'Unable to get an effective response from {}!'.format(url))

    @staticmethod
    def send_message(message):
        '''
        '''
        CONFIG.MESSAGE_QUEUE.put(message)
        pass

    @staticmethod
    def receive_message():
        '''
        '''
        return CONFIG.MESSAGE_QUEUE.get()


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
        '''
        res = {'No': self.curnum, 'urls': urls_dict}
        CONFIG.URL_QUEUE.put(res)
        pass

    def send_none(self):
        '''
        '''
        for _ in range(CONFIG.SPIDER_NUM):
            CONFIG.URL_QUEUE.put(None)

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
        for i in CONFIG.COMPLETE_LIST:
            if i != 0:
                self.curnum = i
            else:
                continue
            res = self.get_url_list()
            self.send_urls_dict(res)
            self.creat_folder()
        self.send_none()
        pass


class ArticleSpider(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        self.r = None
        self.curnum = None
        self.curmp3num = -1
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
            self.curdict = urls_dict['urls']
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
        soup = bs(r.content, 'lxml')
        article = soup.find('div', class_='Content')
        author = article.find('span', class_='byline')
        datetime = article.find('span', class_='datetime')
        res = []
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
        with open(save_to, 'w', encoding='utf-8') as f:
            f.write(self.curtitle)
            f.write('\n')
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
        soup = bs(r.content, 'lxml')
        mp3_url = soup.find('div', class_='menubar')
        try:  # 尝试获取字幕链接
            lrcurl = CONFIG.ROOT_DOMAIN + mp3_url.find('a',
                                                       id='lrc').get('href')
        except AttributeError:
            lrcurl = None
        try:  # 尝试获取翻译链接
            translateurl = CONFIG.ROOT_DOMAIN + r'/VOA_Standard_English/' + mp3_url.find(
                'a', id='EnPage').get('href')
        except AttributeError:
            translateurl = None
        mp3_info_dict = {
            'No': self.curnum,
            'subNo': self.curmp3num,
            'title': self.curtitle,
            'mp3': mp3_url.find('a', id='mp3').get('href'),
            'lrc': lrcurl,
            'translate': translateurl
        }
        return mp3_info_dict

    def get_translate(self, url, save_to):
        '''
        '''
        if url is None:
            return -1
        r = CONFIG.get_html(url)
        r.encoding = 'utf-8'
        soup = bs(r.content, 'lxml')
        article = soup.find('div', class_='Content')
        res = []
        for i in article.find_all('p'):
            res.append(' '.join(i.text.split()))
        with open(save_to, 'w', encoding='utf-8') as f:
            f.write(self.curtitle)
            f.write('\n')
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

    def send_none(self):
        '''
        '''
        for _ in range(CONFIG.SPIDER_NUM):
            CONFIG.MP3_QUEUE.put(None)

    def run(self):
        while True:
            urls_dict = self.get_urls_dict()
            if urls_dict is None:
                break
            else:
                for self.curtitle, self.cururl in self.curdict.items():
                    self.curmp3num += 1
                    self.get_url()
                    self.get_article(
                        r'./week 13/51voa/{}/article/{}.txt'.format(
                            self.curnum,
                            str(self.curmp3num) + ' ' + self.curtitle))
                    mp3_info = self.get_mp3_info()
                    self.get_translate(
                        mp3_info['translate'],
                        r'./week 13/51voa/{}/translate/{}.txt'.format(
                            self.curnum,
                            str(self.curmp3num) + ' ' + self.curtitle))
                    self.send_mp3_info(mp3_info)
        self.send_none()
        pass


class MP3Spider(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        self.curnum = None
        self.curmp3num = None
        self.curtitle = None
        self.curmp3url = None
        self.curlrcurl = None
        self.curmem = None
        self.nonecnt = 0
        pass

    def get_mp3_info(self):
        '''
        '''
        mp3_info = CONFIG.MP3_QUEUE.get()
        if mp3_info is None:
            self.nonecnt += 1
            if self.nonecnt == CONFIG.SPIDER_NUM:
                return None
            return 0
        else:
            self.curnum = mp3_info['No']
            self.curmp3num = mp3_info['subNo']
            self.curtitle = mp3_info['title']
            self.curmp3url = mp3_info['mp3']
            self.curlrcurl = mp3_info['lrc']
            return 1

    def get_music(self, save_to):
        '''
        '''
        r = CONFIG.get_html(self.curmp3url)
        r.encoding = 'utf-8'
        with open(save_to, 'wb') as f:
            f.write(r.content)
            f.flush()
        self.curmem = os.path.getsize(save_to)
        pass

    def get_lrc(self, save_to):
        '''
        '''
        if self.curlrcurl is None:
            return -1
        r = CONFIG.get_html(self.curlrcurl)
        r.encoding = 'utf-8'
        with open(save_to, 'wb') as f:
            f.write(r.content)
            f.flush()
        pass

    def send_mem_info(self):
        '''
        '''
        CONFIG.send_message(self.curmem)
        pass

    def send_none(self):
        '''
        '''
        for _ in range(CONFIG.SPIDER_NUM):
            CONFIG.MESSAGE_QUEUE.put(None)

    def update_mp3_state(self):
        '''
        '''
        CONFIG.COMPLETE_MP3[self.curnum][self.curmp3num] = 0

    def write_md(self):
        '''
        '''
        # 不想写了，要实现也不是不可以...累了累了
        pass

    def run(self):
        while True:
            res = self.get_mp3_info()
            if res is None:
                break
            elif res == 0:
                continue
            else:
                self.get_music(r'./week 13/51voa/{}/mp3/{}.mp3'.format(
                    self.curnum,
                    str(self.curmp3num) + ' ' + self.curtitle))
                self.get_lrc(r'./week 13/51voa/{}/lrc/{}.lrc'.format(
                    self.curnum,
                    str(self.curmp3num) + ' ' + self.curtitle))
                self.send_mem_info()
                self.update_mp3_state()
        self.send_none()
        pass


class SpiderMonitor(Thread):
    '''
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
        '''
        self.run_time = time.time() - CONFIG.START_TIME
        pass

    def etc(self):
        '''
        etc stand for estimated time of completion
        '''
        temp = self.num_of_files * self.run_time / self.cnt_num
        self.remain_time = temp - self.run_time
        pass

    def emc(self):
        '''
        emc stand for estimated memory of completion
        '''
        temp = self.num_of_files * self.cnt_mem / self.cnt_num
        self.remain_mem = temp - self.cnt_mem
        pass

    def get_state(self):
        '''
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
            if flag is None:
                print('Complete')
                break
            os.system('cls')
            stat = '''Run Time : {} s\nSpider Rate : {}/{}\nMemory Usaged : {} MB\nRemain Time : {} s, Remain Menory : {} MB\nNumer of Running Spiders : {}'''.format(
                self.run_time, self.cnt_num, self.num_of_files,
                self.cnt_mem / (1024 * 1024), self.remain_time,
                self.remain_mem / (1024 * 1024),
                CONFIG.SPIDER_NUM - self.nonecnt)
            print(stat)


class SpiderRecovery(Thread):
    '''
    '''
    def __init__(self):
        super().__init__()
        self.id = 0
        pass

    def backup(self, path=r'./week 13/.log'):
        '''
        '''
        CONFIG.refresh_status()
        backup_dict = {
            'id': self.id,
            'time': '{} s'.format(time.time() - CONFIG.START_TIME),
            'state': CONFIG.COMPLETE_LIST
        }
        self.id += 1
        with open(path, 'a+') as f:
            f.write(str(backup_dict))
            f.write('\n')
        print('Back Up at {} s'.format(backup_dict['time']))
        pass

    @staticmethod
    def recovery(path=r'./week 13/.log'):
        '''
        '''
        if not os.path.exists(path):
            raise LogFileNotFoundError('No such log file {} !'.format(path))
        with open(path, 'r') as f:
            lines = f.read().strip().split('\n')
            data = lines[-1]
        if data == '':
            print('No data to recovery')
            return None
        else:
            data = eval(data)
            with CONFIG.LOCK:
                CONFIG.COMPLETE_LIST = data['state']
                for i in range(len(CONFIG.COMPLETE_LIST)):
                    if CONFIG.COMPLETE_LIST[i] == 0:
                        CONFIG.COMPLETE_MP3[i] = [0 for _ in range(50)]
            print('Successfully recovery to time : {}'.format(data['time']))
        pass

    def run(self):
        while True:
            if sum(CONFIG.COMPLETE_LIST) == 0:
                break
            else:
                self.backup()
                time.sleep(30)
        pass


class Master:
    '''
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
        '''
        self._creat_MPS()
        self._creat_AS()
        self._creat_MS()
        self._creat_SM()
        self._creat_SR()
        pass

    def join_all(self):
        '''
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
