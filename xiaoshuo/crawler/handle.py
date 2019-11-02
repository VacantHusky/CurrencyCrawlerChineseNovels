import re
import uuid
from lxml import etree

from queue import Queue
from time import time

# from UI import Ui_MainWindow
from urllib.parse import splittype, splithost

from models import Book
from models.Book import Chapter
from settings import WEB_SETTINGS

book_fields = ['url', 'image', 'title', 'author', 'genre', 'serial', 'word_n', 'info']
chapter_fields = ['url', 'title']


def getRe(txtstr, re_):
    txtre = re.compile(re_)
    txtlist = re.findall(txtre, str(txtstr))
    return txtlist


class BaseHandle:
    html = None
    req = None

    def __init__(self, web):
        self.code = WEB_SETTINGS[web]['code']
        self.web = web

    def setCode(self, response):
        response.encoding = self.code

    def getData(self, response):
        raise NotImplementedError('必须要实现抽象方法：getData()')


class SearchHandle(BaseHandle):
    img_time_out = 5

    def __init__(self, web):
        super().__init__(web)
        self.re_rule = WEB_SETTINGS[web].get('search_re', dict())
        self.xpath_rule = WEB_SETTINGS[web].get('search_xpath', dict())

    def getXpath(self, html, xpath_):
        if self.html is None:
            self.html = etree.HTML(html)
        x = self.html.xpath(xpath_)
        # 过滤标签
        if len(x) > 0 and isinstance(x[0], etree._Element):
            return list(map(lambda i: i.xpath('string(.)'), x))
        else:
            return x

    def handleData(self, response):
        s = response.text
        books_dict = dict()
        books = []
        queue_out = Queue()
        for field in book_fields:
            if self.re_rule.get(field):
                books_dict[field] = getRe(s, self.re_rule[field])
            elif self.xpath_rule.get(field):
                books_dict[field] = self.getXpath(s, self.xpath_rule[field])

        self.req().createImageThread(self.web, books_dict['image'], queue_out)
        print('搜索条目数：', len(books_dict['url']))
        for i in range(len(books_dict['url'])):
            book = Book()
            book.url = books_dict['url'][i].replace(' ', '').replace('\n', '')
            book.image = books_dict['image'][i].replace(' ', '').replace('\n', '')
            book.title = books_dict['title'][i].replace(' ', '').replace('\n', '')
            book.author = books_dict['author'][i].replace(' ', '').replace('\n', '')
            book.genre = books_dict['genre'][i].replace(' ', '').replace('\n', '')
            book.serial = books_dict['serial'][i].replace(' ', '').replace('\n', '')
            book.word_n = books_dict['word_n'][i].replace(' ', '').replace('字', '').replace('\n', '')
            book.info = books_dict['info'][i]
            books.append(book)
        self.booksImage(books, queue_out)
        # Ui_MainWindow.tabWidget.get_ResultWidget('空').label.setText('啊哈哈')
        return books

    def getData(self, response):
        self.html = None
        self.setCode(response)
        return self.handleData(response)

    def booksImage(self, books, queue):
        star_time = time()
        books_n = len(books)
        while time() - star_time < self.img_time_out and books_n > 0:
            if queue.empty():
                continue
            url, path = queue.get()
            if path == 'over':
                continue
            for book in books:
                if book.image == url:
                    book.image = path
                    books_n -= 1
                    break
        print('booksN={}'.format(books_n))


class ImageHandle(BaseHandle):
    # 从response中保存图片
    def getData(self, response):
        img = response.content
        uid = ''.join(str(uuid.uuid4()).split('-'))
        with open('img/{}.jpg'.format(uid), 'wb') as f:
            f.write(img)
        return 'img/{}.jpg'.format(uid)


# 负责处理目录解析
class MenuHandle(BaseHandle):
    chapter_time_out = 5

    def getXpath(self, html, xpath_):
        if self.html is None:
            self.html = etree.HTML(html)
        print(xpath_)
        x = self.html.xpath(xpath_)
        # 过滤标签
        if len(x) > 0 and isinstance(x[0], etree._Element):
            return list(map(lambda i: i.xpath('string(.)'), x))
        else:
            return x

    def __init__(self, web):
        super().__init__(web)
        self.re_rule = WEB_SETTINGS[web].get('chapter_re', dict())
        self.xpath_rule = WEB_SETTINGS[web].get('chapter_xpath', dict())

    def getData(self, response):
        self.html = None
        self.setCode(response)
        return self.handleData(response)

    def handleData(self, response):
        s = response.text
        chapters_dict = dict()
        chapters = []
        queue_out = Queue()
        for field in chapter_fields:
            if self.re_rule.get(field):
                chapters_dict[field] = getRe(s, self.re_rule[field])
            elif self.xpath_rule.get(field):
                chapters_dict[field] = self.getXpath(s, self.xpath_rule[field])
        urls = chapters_dict['url']
        if urls[0] != '' and urls[0][0] == '/' and urls[0][1] != '/':
            menu_url = WEB_SETTINGS[self.web]['menu'].format('')
            proto, rest = splittype(menu_url)
            host, rest = splithost(rest)
            chapters_dict['url'] = [proto + '://' + host + url[:] for url in urls]
        print(chapters_dict)
        # self.req().createChapter(self.web, chapters_dict['url'], queue_out)
        for i in range(len(chapters_dict['url'])):
            chapter = Chapter()
            chapter.url = chapters_dict['url'][i].replace(' ', '')
            chapter.title = chapters_dict['title'][i].replace(' ', '')
            chapter.content = '该章节下载失败'
            chapters.append(chapter)
        # self.dContent(chapters, queue_out)
        # Ui_MainWindow.tabWidget.get_ResultWidget('空').label.setText('啊哈哈')
        return chapters

        # def dContent(self, chapters, queue):
        #     star_time = time()
        #     chapters_n = len(chapters)
        #     while time() - star_time < self.chapter_time_out and chapters_n > 0:
        #         if queue.empty():
        #             continue
        #         id, content = queue.get()
        #         if content == 'over':
        #             continue
        #         chapters[id].content = content
        #         chapters_n -= 1
        #     print('booksN={}'.format(chapters_n))


# 处理一个章节页面
class ChapterHandle(BaseHandle):
    indent = '    '

    def __init__(self, web):
        super().__init__(web)
        self.re_rule = WEB_SETTINGS[web].get('chapter_re', dict())
        self.xpath_rule = WEB_SETTINGS[web].get('chapter_xpath', dict())

    def getData(self, response):
        self.html = None
        self.setCode(response)
        return self.handleData(response)

    def handleData(self, response):
        s = response.text
        if self.re_rule.get('content'):
            content = getRe(s, self.re_rule['content'])
        elif self.xpath_rule.get('content'):
            content = self.getXpath(s, self.xpath_rule['content'])
        if isinstance(content, list):
            content = '\n'.join(content)
        return content

    def getRe(self, txtstr, re_):
        txtre = re.compile(re_)
        txtlist = re.findall(txtre, str(txtstr))
        return self.fuck('\n'.join(txtlist))

    # 这个跟上面几个类的不一样
    def getXpath(self, html, xpath_):
        if self.html is None:
            self.html = etree.HTML(html)
        x = self.html.xpath(xpath_)
        # 过滤标签
        # 此处要兼容各种情况
        if len(x) > 0 and isinstance(x[0], etree._Element):
            content = etree.tostring(x[0], encoding=self.code).decode(self.code)
            print('1', type(content))
        elif len(x) > 0 and isinstance(x[0], str):
            content = "\n".join(x)
            print('2', type(content))
        elif isinstance(x, str):
            content = x
            print('3', type(content))
        else:
            print('未识别的类型：', type(x))
            return x
        return self.fuck(content)

    def fuck(self, content):
        content = content.replace('&#13;', '')
        content = content.replace(' ', '')
        content = content.replace('　', '')  # 全角空格？
        content = content.replace('\t', '')
        content = content.replace('\r\n', '\n')
        content = content.replace('\n\r', '\n')
        content = content.replace('\r', '\n')  # 应该没有单独的\r
        content = content.replace('<p>', '')
        content = content.replace('</p>\n', '\n')
        content = content.replace('</p>', '\n')
        content = content.replace('<br>', '\n')
        content = content.replace('<br/>', '\n')
        content = re.subn('<.*?>', '', content)[0]

        content = content.replace('\n\n', '\n')
        if len(content) > 0 and content[0] == '\n':
            content = content[1:]
        content = content.replace('\n', '\n' + self.indent)
        content = self.indent + content
        return content
