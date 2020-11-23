import abc
import matplotlib.pyplot as plt
import imageio
from numpy.lib.function_base import append
import pkuseg as ps
from mpl_toolkits.mplot3d import Axes3D
import wordcloud.wordcloud as wc
from PIL import Image
import os
import librosa.display as ld
import librosa
import cv2
from sklearn.decomposition import PCA
import random
from faker import Faker


class ZeroDimError(ValueError):
    pass


class TextNotConvertError(ValueError):
    pass


class ImagePathError(ValueError):
    pass


class PlotTypeUnrecognizeError(ValueError):
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
        plt.figure()
        ax1 = plt.axes(projection='3d')
        ax1.plot(x, y, z)
        pass

    def _plot_pca(self, data, *args, **kwargs):
        pca = PCA(n_components=2)
        X_new = pca.transform(data)
        plt.scatter(X_new[:, 0], X_new[:, 1], marker='o', *args, **kwargs)
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
        seg = ps.pkuseg()
        self._cut_text = seg.cut(self._text)
        pass

    def _select_key_words(self):
        with open(r'.\data\stopwords_list.txt', 'r') as f:
            sl = f.read().strip().split('\n')
        self._key_words = []
        for i in self._cut_text:
            if i not in sl:
                self._key_words.append(i)
        pass

    def _wordcloud(self):
        self.wc_ = wc(
            font_path=r'C:\Windows\Fonts\STZHONGS.TTF',  # 设置字体
            background_color="white",  # 背景颜色
            max_words=1000,  # 词云显示的最大词数
            random_state=42,  # 随机数
            collocations=False,  # 避免重复单词
        ).generate(" ".join(self._key_words))
        plt.imshow(self.wc_, interpolation='bilinear')
        plt.axis("off")  # 隐藏坐标
        pass

    def plot(self, data, *args, **kwargs):
        if type(data) == str:
            self._text = data
        elif type(data) == list:
            self._text = self._merge_text(data)
        else:
            raise TextNotConvertError('Can not convet {} to text str'.format(
                type(data)))
        self._cut()
        self._select_key_words()
        self._wordcloud()
        pass


@Plotter.register
class ImagePlotter:
    '''
    '''
    def __init__(self):
        pass

    def _plot_single(self, data: str, *args, **kwargs):
        img = Image.open(data)
        plt.figure()
        plt.axis('off')
        plt.imshow(img)
        plt.show()
        pass

    def _plot_double(self, data: list, *args, **kwargs):
        img1 = Image.open(data[0])
        img2 = Image.open(data[1])
        plt.figure()
        plt.axis('off')
        plt.subplot('121')
        plt.imshow(img1)
        plt.subplot('122')
        plt.imshow(img2)
        plt.show()
        pass

    def _plot_multiple(self, data: list, *args, **kwargs):
        length = kwargs.get('len', 2)
        width = kwargs.get('wid', 2)
        for i in range(int(len(data) / (length * width)) + 1):
            plt.figure()
            plt.axis('off')
            for j in range(length * width):
                plt.subplot(length, width, j + 1)
                if i * (length * width) + j + 1 > len(data):
                    break
                img = Image.open(data[i * (length * width) + j + 1])
                plt.imshow(img)
            plt.show()
        pass

    def _plot_folder(self, data: str, *args, **kwargs):
        img_path_list = []
        img_type_list = ['.jpg', '.png', '.jpeg', '.svg', '.ico', '.gif']
        for root, dirs, files in os.walk(data):
            for file in files:
                if os.path.splitext(file)[1] in img_type_list:
                    img_path_list.append(os.path.join(root, file))
        if len(img_path_list) == 1:
            self._plot_single(img_path_list[0], *args, **kwargs)
        elif len(img_path_list) == 2:
            self._plot_double(img_path_list, *args, **kwargs)
        elif len(img_path_list) == 0:
            print('Nothing to plot.')
            return None
        else:
            self._plot_multiple(img_path_list, *args, **kwargs)
        pass

    def plot(self, data, *args, **kwargs):
        typedata = type(data)
        lendata = len(data)
        if typedata == str:
            if os.path.isfile(data):
                self._plot_single(data, *args, **kwargs)
            elif os.path.isdir(data):
                self._plot_folder(data, *args, **kwargs)
        elif typedata == list:
            if lendata == 1:
                path = data[0]
                if os.path.isfile(path):
                    self._plot_single(path, *args, **kwargs)
                elif os.path.isdir(path):
                    self._plot_folder(path, *args, **kwargs)
            elif lendata == 2:
                self._plot_double(data, *args, **kwargs)
            else:
                self._plot_multiple(data, *args, **kwargs)
        else:
            raise ImagePathError('Cannot match to the Image path')
        pass


@Plotter.register
class GifPlotter:
    '''
    '''
    def __init__(self):
        pass

    def _plot_imglist(self, data: list, *args, **kwargs):
        gif_name = kwargs.get('gif_name', r'img/gif.gif')
        duration = kwargs.get('duration', 0.35)
        frames = []
        for image_name in data:
            frames.append(imageio.imread(image_name))
        imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
        img = Image.open(gif_name)
        plt.figure()
        plt.axis('off')
        plt.imshow(img)
        plt.show()
        pass

    def _plot_folder(self, data: str, *args, **kwargs):
        img_path_list = []
        img_type_list = ['.jpg', '.png', '.jpeg', '.svg', '.ico', '.gif']
        for root, dirs, files in os.walk(data):
            for file in files:
                if os.path.splitext(file)[1] in img_type_list:
                    img_path_list.append(os.path.join(root, file))
        self._plot_imglist(img_path_list, *args, **kwargs)
        pass

    def plot(self, data, *args, **kwargs):
        typedata = type(data)
        lendata = len(data)
        if typedata == str:
            if os.path.isdir(data):
                self._plot_folder(data, *args, **kwargs)
            else:
                raise ImagePathError('String imputed is not a img folder path')
        elif typedata == list:
            if lendata == 1:
                path = data[0]
                if os.path.isfile(path):
                    self._plot_imglist(data, *args, **kwargs)
                elif os.path.isdir(path):
                    self._plot_folder(path, *args, **kwargs)
            else:
                self._plot_imglist(data, *args, **kwargs)
        else:
            raise ImagePathError('Cannot match to the Image path')
        pass


@Plotter.register
class MP3Plotter:
    '''
    '''
    def __init__(self):
        pass

    def plot(self, data, *args, **kwargs):
        music, sr = librosa.load(data)
        plt.figure(figsize=(14, 5))
        ld.waveplot(music, sr=sr)
        plt.show()
        pass


@Plotter.register
class MP4Plotter:
    '''
    '''
    def __init__(self):
        pass

    def _merge_to_gif(self, *args, **kwargs):
        img_path_list = []
        for root, dirs, files in os.walk(r".\MP4data"):
            for file in files:
                img_path_list.append(os.path.join(root, file))
        gif_name = kwargs.get('gif_name', r'img/video2gif.gif')
        duration = kwargs.get('duration', 0.35)
        frames = []
        for image_name in img_path_list:
            frames.append(imageio.imread(image_name))
        imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
        img = Image.open(gif_name)
        plt.figure()
        plt.axis('off')
        plt.imshow(img)
        plt.show()
        pass

    def plot(self, data, *args, **kwargs):
        vidcap = cv2.VideoCapture(data)
        frate = kwargs.get('rate', 30)
        success, image = vidcap.read()
        success = True
        count = 0
        while success:
            try:
                success, image = vidcap.read()
                for _ in range(frate):  # 每 frate 帧进行一次采样
                    vidcap.read()
                cv2.imwrite(r".\MP4data\frame%d.jpg" % count,
                            image)  # save frame as JPEG file
                count += 1
            except cv2.error:
                break
        self._merge_to_gif(*args, **kwargs)
        pass


class PlotAdapter:
    '''
    '''
    def __init__(self):
        pass

    def _plot_point(self, data, *args, **kwargs):
        PointPlotter().plot(data, *args, **kwargs)
        pass

    def _plot_array(self, data, *args, **kwargs):
        ArrayPlotter().plot(data, *args, **kwargs)
        pass

    def _plot_text(self, data, *args, **kwargs):
        TextPlotter().plot(data, *args, **kwargs)
        pass

    def _plot_image(self, data, *args, **kwargs):
        ImagePlotter().plot(data, *args, **kwargs)
        pass

    def _plot_gif(self, data, *args, **kwargs):
        GifPlotter().plot(data, *args, **kwargs)
        pass

    def _plot_mp3(self, data, *args, **kwargs):
        MP3Plotter().plot(data, *args, **kwargs)
        pass

    def _plot_mp4(self, data, *args, **kwargs):
        MP4Plotter().plot(data, *args, **kwargs)
        pass

    def plot(self, data, *args, **kwargs):
        if type(data) == str:
            if os.path.isdir(data):
                self._plot_image(data, *args, **kwargs)
                self._plot_gif(data, *args, **kwargs)
            elif os.path.isfile(data):
                if os.path.splitext(data)[1] == '.mp3':
                    self._plot_mp3(data, *args, **kwargs)
                elif os.path.splitext(data)[1] == '.mp4':
                    self._plot_mp4(data, *args, **kwargs)
                elif os.path.splitext(data)[1] in [
                        '.jpg', '.png', '.jpeg', '.svg', '.ico', '.gif'
                ]:
                    self._plot_image(data, *args, **kwargs)
                    self._plot_gif(data, *args, **kwargs)
                else:
                    PlotTypeUnrecognizeError(
                        'Cannot recognize the plot type by data str you input.'
                    )
            else:
                self._plot_text(data, *args, **kwargs)
            pass
        elif type(data) == list:
            if type(data[0]) == Point:
                self._plot_point(data, *args, **kwargs)
            elif type(data[0]) == list:
                self._plot_array(data, *args, **kwargs)
            elif type(data[0]) == str:
                if os.path.isdir(data[0]) and len(data) == 1:
                    self._plot_image(data, *args, **kwargs)
                    self._plot_gif(data, *args, **kwargs)
                elif os.path.isfile(data[0]):
                    if os.path.splitext(data[0])[1] == '.mp3':
                        self._plot_mp3(data[0], *args, **kwargs)
                    elif os.path.splitext(data[0])[1] == '.mp4':
                        self._plot_mp4(data[0], *args, **kwargs)
                    elif os.path.splitext(data[0])[1] in [
                            '.jpg', '.png', '.jpeg', '.svg', '.ico', '.gif'
                    ]:
                        self._plot_image(data, *args, **kwargs)
                        self._plot_gif(data, *args, **kwargs)
                    else:
                        PlotTypeUnrecognizeError(
                            'Cannot recognize the plot type by data str in list you input.'
                        )
                else:
                    self._plot_text(data, *args, **kwargs)
            else:
                PlotTypeUnrecognizeError(
                    'Cannot recognize the plot type by data list you input.')
        else:
            raise PlotTypeUnrecognizeError(
                'Cannot recognize the plot type by data you input.')
        pass


class GetSomeData:
    '''
    '''
    def __init__(self):
        pass

    def creat_Point(self, num=100):
        '''
        '''
        res = []
        for _ in range(num):
            temp = Point(random.random(), random.random())
            res.append(temp)
        return res

    def creat_Array(self, dim=2, num=100):
        '''
        '''
        res = []
        for _ in range(dim):
            temp = []
            for __ in range(num):
                temp.append(random.random())
            res.append(temp)
        return res

    def creat_Text(self, dim=1, num=1000):
        '''
        '''
        f = Faker('zh-CN')
        if dim == 1:
            res = f.text(num)
        else:
            res = []
            for _ in range(dim):
                res.append(f.text(num))
        return res


class LetWeTest:
    '''
    '''
    def __init__(self):
        self.plot_test = PlotAdapter()
        pass


def main():
    pass


if __name__ == '__main__':
    main()
