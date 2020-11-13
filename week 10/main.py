import random
import matplotlib.pyplot as plt


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
        print('mu:{} x0:{} sigma2:{} N:{}'.format(self.mu, self.x0,
                                                  self.sigma2, self.N))
        pass

    def plot(self):
        '''
        '''
        walk = self.walk()


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
        param_dict['mu'] = random.uniform(1, 100)
        param_dict['x0'] = random.randint(1, 10)
        param_dict['sigma2'] = random.uniform(1, 100)
        param_dict['N'] = N
        return param_dict

    def walks(self):
        '''
        '''
        self._walk_list = []
        N = random.randint(10, 100)
        for i in range(self.num):
            param = RamdonWalks.creat_param_for_walk(N=N)
            print('walk{} params: '.format(i), end='')
            temp = RamdonWalk(**param)
            temp.show_info()
            self._walk_list.append(temp)
        walk_zip = zip(*self._walk_list)
        return walk_zip


def plot_random_walk(walk_zip, save_to=r'./img.png'):
    '''
    '''
    x = [i + 1 for i in range(len(walk_zip))]
    for i in range(len(walk_zip[0])):
        y = [j[i] for j in walk_zip]
        plt.plot(x, y)
    plt.show()


class FaceDataSet:
    '''
    '''
    def __init__(self):
        '''
        '''
        pass

    def __iter__(self):
        '''
        '''
        pass

    def __next__(self):
        '''
        '''
        pass


def main():
    pass


if __name__ == '__main__':
    main()
