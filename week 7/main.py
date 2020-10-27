import re
import os
import sys
import random
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt


class Filter:
    '''
    '''
    def __init__(self, img: Image = '', **kwargs):
        self.img = img
        self.args = kwargs

    def get_img(self):
        '''
        '''
        return self.img

    def set_img(self, new_img):
        '''
        '''
        self.img = new_img
        return None

    def filter(self):
        '''
        '''
        pass


class EdgeExtractionFilter(Filter):
    '''
    '''
    def __init__(self, img, **kwargs):
        super().__init__(self, img, **kwargs)

    def filter(self):
        '''
        '''
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE)
        pass


class SharpenFilter(Filter):
    '''
    '''
    def __init__(self, img, **kwargs):
        super().__init__(self, img, **kwargs)

    def filter(self):
        '''
        '''
        self.img = self.img.filter(ImageFilter.SHARPEN)
        pass


class BlurFilter(Filter):
    '''
    '''
    def __init__(self, img, **kwargs):
        super().__init__(self, img, **kwargs)

    def filter(self):
        '''
        '''
        self.img = self.img.filter(ImageFilter.BLUR)
        pass


class SizeFilter(Filter):
    '''
    '''
    def __init__(self, img, **kwargs):
        super().__init__(self, img, **kwargs)

    def filter(self):
        '''
        '''
        size_ = (self.kwargs['rewidth'], self.kwargs['relength'])
        self.img = self.img.resize(size_, Image.ANTIALIAS)
        pass


class ImageShop:
    '''
    '''
    IMG_TYPE = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

    def __get_img_type(self, name):
        try:
            res = re.search(r'\.[A-Za-z0-9]+$', name).group(0)[1:]
        except AttributeError:
            res = ''
        return res

    def __get_all_img_type(self, name_list):
        res = []
        for i in name_list:
            temp = self.__get_img_type(i)
            if temp and temp not in res:
                res.append(temp)
        return res

    def __get_all_imgs(self, path):
        res = []
        for i, j, k in os.walk(path):
            for l in k:
                if self.__get_img_type(l) in ImageShop.IMG_TYPE:
                    res.append(i + l)
        return res

    def __init__(self, url):
        if url:
            self.img_url = url
            self.imgs = []
            self.img_url_list = self.__get_all_imgs(self, self.img_url)
            self.all_img_type = self.__get_all_img_type(self.img_url_list)
        else:
            self.img_url = url
            self.imgs = []
            self.img_url_list = []
            self.all_img_type = []

    def get_path(self):
        '''
        '''
        return self.img_url

    def set_path(self, path):
        '''
        '''
        self.img_url = path
        self.img_url_list = self.__get_all_imgs(self, self.img_url)
        self.all_img_type = self.__get_all_img_type(self.img_url_list)
        return None

    def load_images(self, img_type):
        '''
        '''
        if img_type not in self.all_img_type:
            print('''Sorry, there are something wrong.
                Either the type you input is not a correct img type,
                or we don't support this img type now.
                Please check and try again.
                ''',
                  file=sys.stderr)
            return None
        for i in self.img_url_list:
            if self.__get_img_type(i) == img_type:
                temp = Image.open(i)
                self.imgs.append(temp)
        return None

    def __batch_ps(self, f: Filter):
        for i in range(len(self.imgs)):
            f.set_img(self.imgs[i])
            f.filter()
            self.imgs[i] = f.get_img()
        return None

    def batch_ps(self, *args):
        '''
        '''
        for i in args:
            if i[0] == 'Blur':
                f = BlurFilter()
                self.__batch_ps(f)
            elif i[0] == 'EdgeExtraction':
                f = EdgeExtractionFilter()
                self.__batch_ps(f)
            elif i[0] == 'Sharpen':
                f = SharpenFilter()
                self.__batch_ps()
            elif i[0] == 'Size':
                keys = {'rewidth': i[1], 'relength': i[2]}
                f = SizeFilter(img='', **keys)
                self.__batch_ps(f)
            else:
                print('''Sorry, there were something wrong.
                Either the type you input is not a correct filter type,
                or we don't support {} filter type now.
                Please check and try again.
                '''.format(i[0]),
                      file=sys.stderr)
                continue
        return None

    def display(self, row=1, col=1, length=0, width=0, maxnum=0):
        '''
        '''
        if maxnum:
            n = maxnum
        else:
            n = min(len(self.imgs), row * col)
        if length and width:
            plt.figure(figsize=(length, width))
        for i in range(1, n + 1):
            plt.subplot(row, col, i)
            plt.inshow(self.img[i - 1])
        plt.show()
        return None

    def save(self, path):
        '''
        '''
        for i in range(len(self.imgs)):
            self.imgs[i].save(path + str(i) + '.jpeg', 'JPEG', quality=95)
        return None


class TestImageShop:
    '''
    '''
    def __init__(self, img_type):
        self.imgshop = ImageShop('')
        self.img_type = img_type

    def load_img_test(self, path):
        '''
        '''
        self.imgshop.set_path(path)
        self.imgshop.load_images(self.img_type)
        return None

    def __make_choice(self):
        choices = ['Blur', 'EdgeExtraction', 'Sharpen', 'Size']
        res = random.choice(choices)
        if res == 'Size':
            return (res, random.randint(1, 10), random.randint(1, 10))
        else:
            return (res)

    def batch_and_display_test(self):
        '''
        '''
        instruction = []
        for i in range(random.randint(1, 10)):
            instruction.append(self.__make_choice())
        print('Process: total:{}'.format(len(instruction)))
        print(*instruction, sep='\n')
        self.imgshop.batch_ps(*instruction)
        display_arg = [random.randint(1, 9), random.randint(1, 9)]
        print('Display: {} × {}'.format(*display_arg))
        self.imgshop.display(*display_arg)

    def save_img_test(self):
        '''
        '''
        os.mkdir(r'./img_after_filter/' + self.img_type + r'_test')
        self.imgshop.save(r'./img_after_filter/' + self.img_type + r'_test/')
        return None


def test(img_type):
    t = TestImageShop(img_type)
    t.load_img_test(r'./img_test')
    t.batch_and_display_test()
    t.save_img_test()


def main():
    for i in ImageShop.IMG_TYPE:
        print('We test {} type now'.format(i))
        test(i)


if __name__ == '__main__':
    main()
