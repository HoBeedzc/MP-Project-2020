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

def creat_param_for_walk(N = 0):
    '''
    '''
    param_dict = {}
    param_dict['mu'] = random.uniform(1,100)
    param_dict['x0'] = random.randint(1,10)
    param_dict['sigma2'] = random.uniform(1,100)
    param_dict['N'] = N
    return param_dict


def random_walks(num):
    '''
    '''
    walk_list = []
    N = random.randint(10,100)
    # make param
    for i in range(num):
        param = creat_param_for_walk(N=N)
        print('walk{} params: '.format(i), param)
        temp = random_walk(**param)
        walk_list.append(temp)
    walk_zip = zip(*walk_list)
    return walk_zip


def plot_random_walk(walk_zip,save_to = r'./img.png'):
    '''
    '''
    x = [i+1 for i in range(len(walk_zip))]
    for i in range(len(walk_zip[0])):
        y = [j[i] for j in walk_zip]
        plt.plot(x,y)
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
