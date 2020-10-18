import time
import sys
from faker import Faker
from pypinyin import lazy_pinyin, Style
from tqdm import tqdm
import random


class Portrait:
    '''
    Portrait class
    properties: url, length, wide
    methods: get_url, get_len, get_wid, set_url, set_len, set_wid
    '''
    def __init__(self, url, length, wide):
        self.url = url
        self.len = length
        self.wid = wide

    def get_url(self):
        '''
        获取图像url地址
        :param self: 图像类的实例对象
        :return: 图像url地址
        '''
        return self.url

    def get_len(self):
        '''
        获取图像长度
        :param self: 图像类的实例对象
        :return: 图像长度
        '''
        return self.len

    def get_wid(self):
        '''
        获取图像宽度
        :param self: 图像类的实例对象
        :return: 图像宽度
        '''
        return self.wid

    def set_url(self, value):
        '''
        设置图像url地址
        :param self: 图像类的实例对象
        :param value: 修改后的值
        :return: None
        '''
        self.url = value
        return None

    def set_len(self, value):
        '''
        设置图像长度
        :param self: 图像类的实例对象
        :param value: 修改后的值
        :return: None
        '''
        self.len = value
        return None

    def set_wid(self, value):
        '''
        设置图像宽度
        :param self: 图像类的实例对象
        :param value: 修改后的值
        :return: None
        '''
        self.wid = value
        return None


class Contact:
    '''
    Contact class
    properties: id, name, tel, email, portrait
    methods: get_id, get_name, get_tel, get_email, get_portrait, set_name, set_tel, set_email, set_portrait, show_contact
    '''
    ID = 0

    def __init__(self, name: str, tel: str, email: str, portrait='', cid=''):
        if type(cid) == int:
            self.id = cid
        else:
            if cid != '':
                print('id is not correct! we will set a default id.')
            self.id = Contact.ID
            Contact.ID += 1
        self.name = name
        self.tel = tel
        self.email = email
        self.portrait = portrait

    def get_id(self):
        '''
        获取联系人id
        :param self: 联系人实例对象
        :return: 联系人id
        '''
        return self.id

    def get_name(self):
        '''
        获取联系人姓名
        :param self: 联系人实例对象
        :return: 联系人姓名
        '''
        return self.name

    def get_tel(self):
        '''
        获取联系人电话
        :param self: 联系人实例对象
        :return: 联系人电话
        '''
        return self.tel

    def get_email(self):
        '''
        获取联系人邮箱
        :param self: 联系人实例对象
        :return: 联系人邮箱
        '''
        return self.email

    def get_portrait(self):
        '''
        获取联系人头像
        :param self: 联系人实例对象
        :return: 联系人头像
        '''
        return self.portrait

    def set_name(self, value):
        '''
        设置联系人姓名
        :param self: 联系人实例对象
        :param value: 修改后的值
        :return: None
        '''
        self.name = value
        return None

    def set_tel(self, value):
        '''
        设置联系人电话
        :param self: 联系人实例对象
        :param value: 修改后的值
        :return: None
        '''
        self.tel = value
        return None

    def set_email(self, value):
        '''
        设置联系人邮箱
        :param self: 联系人实例对象
        :param value: 修改后的值
        :return: None
        '''
        self.email = value
        return None

    def set_portrait(self, value):
        '''
        设置联系人头像
        :param self: 联系人实例对象
        :param value: 修改后的值
        :return: None
        '''
        self.portrait = value
        return None

    def show_contact(self):
        '''
        输出联系人
        :param self: 联系人实例对象
        :return: None
        '''
        print('id:{}\tname:{}\ttel:{}\temail:{}'.format(
            self.get_id(), self.get_name(), self.get_tel(), self.get_email()))
        return None


class ContactBook:
    '''
    ContactBook class
    properties: contacts, num
    methods: add_contact, update_contact, delete_contact, search_contact, sorted_output
    '''
    def __init__(self):
        self.contacts = []
        self.num = 0

    def add_contact(self, contact: Contact):
        '''
        添加联系人 重复添加会报错
        :param self: 通讯录实例
        :param contact: 联系人实例
        :return: None
        '''
        flag = 1
        for i in self.contacts:
            if i['contact'].email == contact.email and i[
                    'contact'].tel == contact.tel:
                print('Repeat contact!', file=sys.stderr)
                flag = 0
                break
        if flag:
            res = {'contact': contact}
            res['init time'] = time.ctime()
            res['update time'] = time.ctime()
            self.contacts.append(res)
            self.num += 1
        return None

    def update_contact(self, old_contact, new_contact):
        '''
        更新联系人 更新不存在的联系人会报错
        :param self: 通讯录实例
        :param old_contact: 要修改的联系人实例
        :param new_contact: 修改后的联系人实例
        :return: None
        '''
        flag = 1
        for i in self.contacts:
            if i['contact'] == old_contact:
                i['contact'] = new_contact
                i['update time'] = time.ctime()
                flag = 0
                break
        if flag:
            print('Sorry, no such contact has been found!', file=sys.stderr)
        return None

    def delete_contact(self, contact):
        '''
        删除联系人 删除不存在的联系人会报错
        :param self: 通讯录实例
        :param contact: 联系人实例
        :return: None
        '''
        flag = 1
        for i in range(self.num):
            if self.contacts[i]['contact'] == contact:
                del self.contacts[i]
                self.num -= 1
                flag = 0
                break
        if flag:
            print('Sorry, no such contact has been found!', file=sys.stderr)
        return None

    def search_contact(self, by_value, value, exact=False):
        '''
        通讯录搜索
        :param self: 通讯录实例
        :param by_value: 要搜索属性
        :param value: 要搜索的值
        :param exact: 是否精确匹配 默认关闭
        :return: 符合条件的搜索结果
        '''
        if self.num == 0:
            print('Sorry, contactbook empyted!', file=sys.stderr)
            return []
        if by_value not in self.contacts[0]['contact'].__dict__.keys():
            print('Sorry, no such property!', file=sys.stderr)
            return []
        result = []
        if exact:
            for i in self.contacts:
                if str(i['contact'].__dict__[by_value]) == str(value):
                    result.append(i['contact'])
        else:
            for i in self.contacts:
                if str(value) in str(i['contact'].__dict__[by_value]):
                    result.append(i['contact'])
        return result

    def sorted_output(self, by_value, reverse=False, show=False):  # #fff
        '''
        通讯录排序输出
        :param self: 通讯录实例
        :param by_value: 要进行排序的属性
        :param reverse: False for 升序 True for 降序
        :return: None (排序结果会直接输出)
        '''
        if self.num == 0:
            print('Sorry, contactbook empyted!', file=sys.stderr)
            return None
        if by_value not in self.contacts[0]['contact'].__dict__.keys():
            print('Sorry, no such property!', file=sys.stderr)
            return None
        result = sorted(self.contacts,
                        key=lambda x: x['contact'].__dict__[by_value],
                        reverse=reverse)
        print('Result: sorted by {}, reverse = {}'.format(by_value, reverse))
        if show:
            for i in result:
                print('Contact:', end='')
                i['contact'].show_contact()
                # print('init time:{}\tupdate time:{}'.format(i['init time'], i['update time']))
        return None

    def search_contact_by_pinyin(self, value, exact=False):
        '''
        通讯录搜索 按拼音搜索姓名
        :param self: 通讯录实例
        :param value: 要搜索的值
        :param exact: 是否精确匹配 默认关闭
        :return: 符合条件的搜索结果
        '''
        if self.num == 0:
            print('Sorry, contactbook empyted!', file=sys.stderr)
            return []
        result = []
        if exact:
            for i in self.contacts:
                if ''.join(
                        lazy_pinyin(i['contact'].name,
                                    style=Style.FIRST_LETTER)) == value:
                    result.append(i['contact'])
        else:
            for i in self.contacts:
                if value in ''.join(
                        lazy_pinyin(i['contact'].name,
                                    style=Style.FIRST_LETTER)):
                    result.append(i['contact'])
        return result

    def save_contact(self, path):
        '''
        保存通讯录
        :param self: 通讯录实例
        :param path: 要保存的路径
        :return: None
        '''
        with open(path, 'w') as f:
            f.write('id,name,tel,email,init time,update time\n')
            for i in self.contacts:
                f.write('{},{},{},{},{},{}'.format(
                    i['contact'].id, i['contact'].name, i['contact'].tel,
                    i['contact'].email, i['init time'], i['update time']))
                f.write('\n')
        return None

    def read_contact(self, path):
        '''
        加载通讯录 会直接覆盖原来的通讯录
        :param self: 通讯录实例
        :param path: 要加载的路径
        :return: None
        '''
        self.num = 0
        self.contacts = []
        with open(path, 'r') as f:
            f.readline()
            for i in f.read().strip().split('\n')[:-1]:
                res = {}
                tempcontact = Contact(i[1], i[2], i[3], cid=int(i[0]))
                res['contact'] = tempcontact
                res['init time'] = i[4]
                res['update time'] = i[5]
                self.contacts.append(res)
                self.num += 1
        return None


class ContactTest:
    '''
    '''
    def __init__(self, lan='zh_CN'):
        self.contactbook = ContactBook()
        self.lan = lan

    def add_contact_test(self, num):
        '''
        加入联系人测试
        :param self: 测试实例
        :param num: 加入联系人数量
        :return: None
        '''
        start = time.time()
        fake = Faker(locale=self.lan)
        for i in tqdm(range(num)):
            fake_portrait_temp = [
                fake.image_url(),
                fake.pyint(min_value=1, max_value=9999, step=1),
                fake.pyint(min_value=0, max_value=9999, step=1)
            ]
            portrait_temp = Portrait(*fake_portrait_temp)
            fake_contact_temp = [
                fake.name(),
                fake.phone_number(),
                fake.email(), portrait_temp
            ]
            contact_temp = Contact(*fake_contact_temp)
            self.contactbook.add_contact(contact_temp)
        end = time.time()
        print('Running time: %s Seconds' % (end - start))
        return None

    def sort_contact_test(self):
        '''
        联系人排序测试
        :param self: 测试实例
        :return: None
        '''
        start = time.time()
        for i in tqdm(['id', 'name', 'tel', 'email']):
            for j in [True, False]:
                start1 = time.time()
                print('Sorted by {} reverse = {}'.format(i, j))
                self.contactbook.sorted_output(by_value=i, reverse=j)
                end1 = time.time()
                print('Running time: %s Seconds' % (end1 - start1))
                print()
        end = time.time()
        print('Total running time: %s Seconds' % (end - start))
        return None

    def search_contact_test(self):
        '''
        联系人搜索测试
        :param self: 测试实例
        :return: None
        '''
        start = time.time()
        for i in tqdm(['id', 'name', 'tel', 'email']):
            for j in [True, False]:
                if j:
                    search_temp = self.contactbook.contacts[random.randint(
                        1, self.contactbook.num - 1)]['contact'].__dict__[i]
                else:
                    search_temp = str(self.contactbook.contacts[random.randint(
                        1, self.contactbook.num - 1)]['contact'].__dict__[i])
                    search_temp = search_temp[:random.
                                              randint(1, len(search_temp))]
                start1 = time.time()
                print('Search by {} exactly = {}, search for {}'.format(
                    i, j, search_temp))
                for k in self.contactbook.search_contact(by_value=i,
                                                         value=search_temp,
                                                         exact=j):
                    k.show_contact()
                end1 = time.time()
                print('Running time: %s Seconds' % (end1 - start1))
                print()
        end = time.time()
        print('Total running time: %s Seconds' % (end - start))
        return None

    def search_contact_by_pinyin_test(self):
        '''
        联系人拼音搜索测试
        :param self: 测试实例
        :return: None
        '''
        start = time.time()
        for j in [True, False]:
            if j:
                search_temp = 'lzq'
            else:
                search_temp = 'lz'
            start1 = time.time()
            print('Search for {1} exactly = {0}'.format(j, search_temp))
            for k in self.contactbook.search_contact_by_pinyin(
                    value=search_temp, exact=j):
                k.show_contact()
            end1 = time.time()
            print('Running time: %s Seconds' % (end1 - start1))
            print()
        end = time.time()
        print('Total running time: %s Seconds' % (end - start))
        return None

    def save_contact_test(self):
        '''
        联系人保存读取测试
        :param self: 测试实例
        :return: None
        '''
        start = time.time()
        self.contactbook.save_contact(r'.\data\hobee_contact_{}.csv'.format(
            self.lan))
        self.contactbook.read_contact(r'.\data\hobee_contact_{}.csv'.format(
            self.lan))
        end = time.time()
        print('Running time: %s Seconds' % (end - start))
        return None


def test(lan):
    t = ContactTest(lan=lan)
    t.add_contact_test(5000)
    t.sort_contact_test()
    t.search_contact_test()
    t.search_contact_by_pinyin_test()
    t.save_contact_test()


def main():
    test('zh_CN')
    test('en_US')


if __name__ == '__main__':
    main()
