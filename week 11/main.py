import abc
import matplotlib.pyplot as plt
import pkuseg as ps
from mpl_toolkits.mplot3d import Axes3D
import wordcloud as wc
from PIL import Image


class ZeroDimError(ValueError):
    pass


class Plotter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def plot(self, data, *args, **kwargs):
        pass


class Point:
    '''
    '''
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x
        pass

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y
        pass


@Plotter.register
class PointPlotter:
    '''
    '''
    def __init__(self):
        pass

    def plot(self, data, *args, **kwargs):
        x = [i.x for i in data]
        y = [i.y for i in data]
        plt.scatter(x, y, *args, **kwargs)
        pass


@Plotter.register
class ArrayPlotter:
    '''
    '''
    def __init__(self):
        pass

    def _plot2d(self, data, *args, **kwargs):
        x = data[0]
        y = data[1]
        plt.plot(x, y, *args, **kwargs)
        pass

    def _plot3d(self, data, *args, **kwargs):
        x = data[0]
        y = data[1]
        z = data[2]
        fig = plt.figure()
        ax1 = plt.axes(projection='3d')
        ax1.plot(x, y, z)
        pass

    def _plot_pca(self, data, *args, **kwargs):
        pass

    def plot(self, data, *args, **kwargs):
        length = len(data)
        if length == 0:
            raise ZeroDimError('Can not plot data with dim zero.')
        elif length == 1:
            x = [i + 1 for i in range(len(data[0]))]
            self._plot2d(self, [x, data[0]], *args, **kwargs)
        elif length == 2:
            self._plot2d(self, data, *args, **kwargs)
        elif length == 3:
            self._plot3d(self, data, *args, **kwargs)
        else:
            self._plot_pca(self, data, *args, **kwargs)
        pass


@Plotter.register
class TextPlotter:
    '''
    '''
    def __init__(self):
        pass

    @staticmethod
    def _merge_text(data):
        ans = ''
        for i in data:
            try:
                ans += str(i) + ''
            except ValueError:
                continue
        return ans

    def _cut(self):
        pass

    def plot(self, data, *args, **kwargs):
        pass


@Plotter.register
class ImagePlotter:
    '''
    '''
    def __init__(self):
        pass

    def _plot_single(self):
        pass

    def _plot_multiple(self):
        pass

    def _plot_folder(self):
        pass

    def plot(self, data, *args, **kwargs):
        pass


@Plotter.register
class GifPlotter:
    '''
    '''
    def __init__(self):
        pass

    def plot(self, data, *args, **kwargs):
        pass


@Plotter.register
class MP3Plotter:
    '''
    '''
    def __init__(self):
        pass

    def plot(self, data, *args, **kwargs):
        pass


class GetSomeData:
    '''
    '''
    def __init__(self):
        pass


class LetWeTest:
    '''
    '''
    def __init__(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
