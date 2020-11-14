import re
import os
import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class ImageNotExistError(FileNotFoundError):
    pass


class RamdonWalk:
    '''
    '''
    def __init__(self, mu, x0, sigma2, N):
        self._mu = mu
        self._x0 = x0
        self._sigma2 = sigma2
        self._N = N

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, new_mu):
        self._mu = new_mu

    @mu.deleter
    def mu(self):
        self._mu = 0

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, new_x0):
        self._x0 = new_x0

    @x0.deleter
    def x0(self):
        self._x0 = 0

    @property
    def sigma2(self):
        return self._sigma2

    @sigma2.setter
    def sigma2(self, new_sigma2):
        self._sigma2 = new_sigma2

    @sigma2.deleter
    def sigma2(self):
        self._sigma2 = 0

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, new_N):
        self._N = new_N

    @N.deleter
    def N(self):
        self._N = 0

    def walk(self):
        '''
        '''
        cnt = 0
        wt = random.gauss(0, sigma=self.sigma2)
        x0 = self.x0
        while cnt < self.N:
            x = self.mu + x0 + wt
            yield x
            x0 = x
            wt = random.gauss(0, sigma=self.sigma2)
            cnt += 1
        return 'Complete'

    def show_info(self):
        '''
        '''
        paramstr = 'mu:{} x0:{} sigma2:{} N:{}'.format(self.mu, self.x0,
                                                       self.sigma2, self.N)
        print(paramstr)
        return paramstr

    def plot(self):
        '''
        '''
        walk = self.walk()
        x = [i + 1 for i in range(self.N)]
        y = [i for i in walk]
        plt.plot(x, y)
        plt.text(0, max(y), self.show_info())
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('A Random Walk')
        plt.show()


class RamdonWalks:
    '''
    '''
    def __init__(self, walks_num):
        self._num = walks_num
        self._walk_list = []

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, new_num):
        self._num = new_num

    @num.deleter
    def num(self):
        self._num = 0

    @staticmethod
    def creat_param_for_walk(N=0):
        '''
        '''
        param_dict = {}
        param_dict['mu'] = random.uniform(1, 10)
        param_dict['x0'] = random.randint(1, 100)
        param_dict['sigma2'] = random.uniform(1, 100)
        param_dict['N'] = N
        return param_dict

    def walks(self):
        '''
        '''
        self._walk_list = []
        N = 500
        for i in range(self.num):
            param = RamdonWalks.creat_param_for_walk(N=N)
            print('walk{} params: '.format(i), end='')
            temp = RamdonWalk(**param)
            temp.show_info()
            self._walk_list.append(temp.walk())
        walk_zip = zip(*self._walk_list)
        return walk_zip

    def plots(self):
        '''
        '''
        walk_zip = list(self.walks())
        x = [i + 1 for i in range(len(walk_zip))]
        for i in range(len(walk_zip[0])):
            y = [j[i] for j in walk_zip]
            plt.plot(x, y, label='walk {}'.format(i))
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Random Walks')
        plt.show()


class FaceDataSet:
    '''
    '''
    IMGINFO_DICT = {'ftw': 750, 'fty': 2000, 'mtw': 750, 'mty': 2000}

    def _check_path(self):
        flag = 1
        for i in os.listdir(self.path):
            try:
                res = re.search(r'\.[A-Za-z0-9]+$', i).group(0)[1:]
            except AttributeError:
                res = ''
            if res == 'jpg':
                flag = 0
        if flag:
            raise ImageNotExistError(
                'There no .jpg file in path {}. Path will reset!'.format(
                    self.path))
        else:
            print('Find .jpg in path {} successfully!'.format(self.path))
        pass

    def __init__(self,
                 ipath=r'./dataset/FaceImages/Images/',
                 start=0,
                 end=5500):
        '''
        '''
        self._path = ipath
        self._check_path()
        self._start = start
        self._end = end
        pass

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path
        self._check_path()
        pass

    @path.deleter
    def path(self):
        self._path = r'./'
        pass

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, new_start):
        self._start = new_start

    @start.deleter
    def start(self):
        self._start = 0

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, new_end):
        self._end = new_end

    @end.deleter
    def end(self):
        self._end = 5500

    def show_ndarray(self, show=False):
        '''
        '''
        if self.cnt <= self.IMGINFO_DICT['ftw']:
            self.cntname = self.path + r'ftw{}.jpg'.format(self.cnt)
            self.cntimg = Image.open(self.cntname)
        elif self.cnt <= self.IMGINFO_DICT['ftw'] + self.IMGINFO_DICT['fty']:
            self.cntname = self.path + r'fty{}.jpg'.format(
                self.cnt - self.IMGINFO_DICT['ftw'])
            self.cntimg = Image.open(self.cntname)
        elif self.cnt <= self.IMGINFO_DICT['ftw'] + self.IMGINFO_DICT[
                'fty'] + self.IMGINFO_DICT['mtw']:
            self.cntname = self.path + r'mtw{}.jpg'.format(
                self.cnt - self.IMGINFO_DICT['ftw'] - self.IMGINFO_DICT['fty'])
            self.cntimg = Image.open(self.cntname)
        else:
            self.cntname = self.path + r'mty{}.jpg'.format(
                self.cnt - self.IMGINFO_DICT['ftw'] -
                self.IMGINFO_DICT['fty'] - self.IMGINFO_DICT['mtw'])
            self.cntimg = Image.open(self.cntname)
        self.cntarray = np.array(self.cntimg)
        if show:
            print(self.cntarray)
            plt.imshow(self.cntimg)
            plt.show()
        return self.cntname

    def __iter__(self):
        '''
        '''
        self.cnt = self.start
        return self

    def __next__(self):
        '''
        '''
        if self.cnt < self.end:
            self.cnt += 1
            return self.show_ndarray(show=True)
        else:
            raise StopIteration('全部加载完成！')


class BaseTest:
    '''
    '''
    def __init__(self):
        self.rws = RamdonWalks(random.randint(2, 8))
        self.rw = RamdonWalk(**self.rws.creat_param_for_walk(N=500))
        self.fdw = FaceDataSet(start=100, end=110)

    def rw_test(self):
        '''
        '''
        print('Show random walk info...')
        self.rw.show_info()
        self.rw.walk()
        self.rw.plot()
        pass

    def rws_test(self):
        '''
        '''
        self.rws.plots()
        pass

    def fdw_test(self):
        '''
        '''
        for i in self.fdw:
            print('Open {} successfully!'.format(i))
        pass


def main():
    test = BaseTest()
    test.rw_test()
    test.rws_test()
    test.fdw_test()
    pass


if __name__ == '__main__':
    main()
