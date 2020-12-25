import asyncio
import os
import re
import sys
import time


class SearchTypeError(ValueError):
    pass


class CONFIG:
    """
    some global config and variables
    """
    TEXT_FILE = ['.txt', '.csv', '.java', '.c', '.py', '.md', '.tex', '.sql']
    WORD_FILE = ['.doc', '.docx']
    EXCEL_FILE = ['.xls', 'xlsx']
    PPT_FILE = ['.ppt', '.pptx']
    PDF_FILE = ['.pdf']
    KEY_TYPE = TEXT_FILE
    KEY_WORD = 'HoBee'
    IF_TITLE = True
    FLOAT_LENGTH = 20
    ROOT_PATH = './'
    SEARCHED_FILES = 0
    OPENED_FILES = 0
    READ_LINES = 0


class Result:
    """
    a class for search result which used in this file
    instance variables: id, name, path, line, content
    """
    ID = 0

    def __init__(self, name, path, line, content):
        self.id = Result.ID
        Result.ID += 1
        self.name = name
        self.path = path
        self.line = line
        self.content = content
        pass


class Searcher:
    """
    a class for searching files in harddisk
    """

    def __init__(self):
        pass

    @staticmethod
    async def search():
        """
        """
        path = CONFIG.ROOT_PATH
        g = os.walk(path)
        for _dir, _, files in g:
            for file in files:
                CONFIG.SEARCHED_FILES += 1
                ext = os.path.splitext(file)[-1]
                if ext in CONFIG.KEY_TYPE:
                    file_path = os.path.join(_dir, file)
                    await TextOpener.open(file_path)  # 传值给别的生成器
                else:
                    continue
        pass


class Opener:
    """
    a parent class for open files
    """

    def __init__(self):
        pass

    @staticmethod
    async def _check_title(filepath):
        fname, etx = os.path.splitext(filepath)
        fname = fname.replace('\\', '/')  # 解决win和mac运行时的兼容性问题
        name_ = fname.split('/')[-1] + etx
        res = re.search(CONFIG.KEY_WORD, name_)
        if res is None:
            pass
        else:
            resc = Result(name_, filepath, 'title', name_)
            await Hitter.hit(resc)
        pass

    @staticmethod
    def open(filepath):
        pass


class TextOpener(Opener):
    """
    a subclass for open flies which used for text file
    """

    def __init__(self):
        super(TextOpener, self).__init__()
        pass

    @staticmethod
    async def open(filepath):
        # print(filepath)
        if CONFIG.IF_TITLE:
            await TextOpener._check_title(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                CONFIG.OPENED_FILES += 1
                await TextReader.read(filepath, f)
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='gbk') as f:
                    CONFIG.OPENED_FILES += 1
                    await TextReader.read(filepath, f)
            except UnicodeDecodeError:
                # print('UnicodeDecodeError:{}'.format(filepath))
                pass
        except FileNotFoundError:
            # print('FileNotFoundError:{}'.format(filepath))
            pass
        except OSError:
            # print('OSError:{}'.format(filepath))
            pass
        pass


class WordOpener(Opener):
    pass


class ExcelOpener(Opener):
    pass


class PPTOpener(Opener):
    pass


class PDFOpener(Opener):
    pass


class Reader:
    """
    a parent class for read files
    """

    def __init__(self):
        pass

    @staticmethod
    def read(filepath, f):
        pass


class TextReader(Reader):
    """
    a subclass for read files which used for text files
    """

    def __init__(self):
        super(TextReader, self).__init__()
        pass

    @staticmethod
    async def read(filepath, f):
        i = 0
        for line in f:
            i += 1
            line = line.strip()
            flag = await Judger.judge(filepath, i, line)
            if flag:
                break
            else:
                continue


class Judger:
    """
    a class for judging the file whether include key words or not
    """

    def __init__(self):
        pass

    @staticmethod
    async def judge(filepath,
                    line_number,
                    content,
                    search_for=CONFIG.KEY_WORD):
        CONFIG.READ_LINES += 1
        res = re.search(search_for, content)
        if res is None:
            return 0
        else:
            li, ri = res.span()
            li_n = max(0, li - CONFIG.FLOAT_LENGTH)
            ri_n = min(len(content), ri + CONFIG.FLOAT_LENGTH)
            new_con = content[li_n:li] + '==' + res.group(
                0) + '==' + content[ri:ri_n + 1]
            fname, etx = os.path.splitext(filepath)
            fname = fname.replace('\\', '/')
            name_ = fname.split(r'/')[-1] + etx
            resc = Result(name_, filepath, line_number, new_con)
            await Hitter.hit(resc)
            return 1
        pass


class WordJudger(Judger):
    pass


class ExcelJudger(Judger):
    pass


class PPTJudger(Judger):
    pass


class PDFJudger(Judger):
    pass


class Hitter:
    """
    a class for show the search result to users
    """

    def __init__(self):
        pass

    @staticmethod
    async def hit(resc):
        print('{}, {}, {}, {}, {}'.format(resc.id, resc.name, resc.path,
                                          resc.line, resc.content))
        pass


class LoaclMiner:
    """
    a main class for this program
    """

    def __init__(self, path='', type_='', search_for='', float_='', stype=''):
        self.path = path
        self.type = type_
        self.search_for = search_for
        self.float = float_
        self.search_type = stype
        pass

    def _set_config(self):
        if self.path != '':
            CONFIG.ROOT_PATH = self.path
        if self.float != '':
            CONFIG.FLOAT_LENGTH = self.float
        if self.search_for != '':
            CONFIG.KEY_WORD = self.search_for
        if self.search_type != '':
            CONFIG.IF_TITLE = self.search_type
        if self.type != '':
            all_type = [
                CONFIG.TEXT_FILE, CONFIG.WORD_FILE, CONFIG.EXCEL_FILE,
                CONFIG.PPT_FILE, CONFIG.PDF_FILE
            ]
            if self.type in ['0', '1', '2', '3', '4']:
                CONFIG.KEY_TYPE = all_type[int(self.type)]
            else:
                try:
                    new_type = re.search(r'\.[A-Za-z0-9]+$',
                                         self.type).group(0)
                except AttributeError:
                    raise SearchTypeError('Can not find {} file!'.format(
                        self.type))
                CONFIG.KEY_WORD = [new_type]

    def _async_loop(self):
        self.loop = asyncio.get_event_loop()
        self.tasks = [Searcher.search()]
        self.loop.run_until_complete(asyncio.wait(self.tasks))
        self.loop.close()
        pass

    @staticmethod
    def _summary(end, start):
        print('Summary:')
        print('Search time : {}'.format(end - start))
        print('Search Files : {}'.format(CONFIG.SEARCHED_FILES))
        print('Open Files : {}'.format(CONFIG.OPENED_FILES))
        print('Read Lines : {}'.format(CONFIG.READ_LINES))
        print('Find Result : {}'.format(Result.ID - 1))

    def start(self):
        self._set_config()
        print('Start to search {} in {} file from path {} ...'.format(
            CONFIG.KEY_WORD, CONFIG.KEY_TYPE, CONFIG.ROOT_PATH))
        print('Result:')
        print('ID, NAME, PATH, LINE NUMBER, CONTENT')
        start = time.time()
        self._async_loop()
        end = time.time()
        self._summary(end, start)
        pass


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        path = ''
    try:
        type_ = sys.argv[2]
    except IndexError:
        type_ = ''
    try:
        search_for = sys.argv[3]
    except IndexError:
        search_for = ''
    try:
        stype = sys.argv[4]
    except IndexError:
        stype = ''
    try:
        float_ = int(sys.argv[5])
    except IndexError:
        float_ = ''
    test = LoaclMiner(path, type_, search_for, float_, stype)
    test.start()
    pass


if __name__ == '__main__':
    main()
    pass
