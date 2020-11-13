import random
import matplotlib.pyplot as plt


def random_walk(mu, x0, sigma2, N):
    '''
    '''
    cnt = 0
    wt = random.gauss(0, sigma=sigma2)
    while cnt < N:
        x = mu + x0 + wt
        yield x
        x0 = x
        wt = random.gauss(0, sigma=sigma2)
        cnt += 1
    return 'Complete'


def random_walks(num):
    '''
    '''
    pass


def plot_random_walk():
    '''
    '''
    pass


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
