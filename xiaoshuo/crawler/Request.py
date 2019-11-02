import os
import requests
import threading, time
from queue import Queue
from urllib.parse import quote

import sys

from crawler.Middleware import UserAgentMiddleware
from crawler.handle import SearchHandle, ImageHandle, BaseHandle, MenuHandle, ChapterHandle
# from crawler.showData import SearchShow
from settings import WEB_SETTINGS, IS_QT5, Exemption


# 专门用来发送请求的线程
# addheader ： 用来提供请求头
# handle_response ：从response提取出数据
class ReqThread(threading.Thread):
    is_over = False
    bad_urls = []
    bad_time = 3
    bad_count = 3
    time_out = 7

    addheader = UserAgentMiddleware().process_request
    handle_response = None

    def __init__(self, web, queue_in, queue_out, single=False, re_fun=None, handle_response=None):
        threading.Thread.__init__(self)
        self.web = web
        self.queue = queue_in
        self.queue_out = queue_out
        self.single = single
        self.re_fun = re_fun
        self.handle_response = handle_response

    def run(self):
        print('开始爬取')
        while not self.is_over:
            if self.queue.empty() and len(self.bad_urls) <= 0:
                continue

            # 从队列或坏队列中取url
            if not self.queue.empty():
                id, url = self.queue.get()
                count = 0
                print('id:{},爬取：{}'.format(id, url))
            elif len(self.bad_urls) > 0:
                if time.time() - self.bad_urls[0][1] > self.bad_time:
                    id, url, _, count = self.bad_urls.pop(0)
                    print('旧的url:{}'.format(url))
                else:
                    continue

            if url == 'over':
                self.is_over = True
                print('线程{}退出'.format(id))
                continue

            self.doSamething(id, url)
            # try:
            #     self.doSamething(url)
            # except Exception as e:
            #     print('error:', e)
            #     if count + 1 < self.bad_count:
            #         self.bad_urls.append((id, url, time.time(), count + 1))

            if self.single:
                print('单次线程结束')
                self.is_over = True
        print('线程over')
        self.queue_out.put((self.web, 'over'))

    def doSamething(self, id, url):
        # 设置头部
        headers = dict()
        self.addheader(headers, self.web, url)
        # 发送请求
        response = requests.get(url, headers=headers, timeout=self.time_out)
        # 处理数据
        if self.handle_response:
            r = self.handle_response.getData(response)
            self.queue_out.put((id, r))
        else:
            self.queue_out.put((id, response))


# 用来解析任务，创建线程
class Request:
    search_handle = SearchHandle
    image_handle = ImageHandle
    down_handle = MenuHandle

    def __init__(self):
        pass

    # 单例
    def __new__(cls, *args, **kwargs):
        print('初始化')
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    # 创建一个搜索线程
    def createSearchThread(self, web, search_word, queue_out=None):
        queue_1 = Queue()
        if queue_out is None:
            queue_2 = Queue()
        else:
            queue_2 = queue_out
        queue_1.put((web, WEB_SETTINGS[web]['search'].format(quote(search_word))))
        ReqThread(web, queue_1, queue_2, single=True, handle_response=self.search_handle(web)).start()

        if IS_QT5:
            return queue_2
            # SearchShow(web, queue_2)

    # 创建一个搜索图片的线程
    # 给一个列表，列表中存放url
    # 还得给一个队列，图片存储的路径会放在队列里
    def createImageThread(self, web, urls, queue_out):
        for url in urls:
            queue = Queue()
            queue.put((url, url))
            ReqThread(web, queue, queue_out, single=True, handle_response=self.image_handle(web)).start()
            # return queue_out

    def createDownTxt(self, web, book, queue_out=None):
        queue_1 = Queue()
        queue_2 = Queue()
        if queue_out is None:
            queue_3 = Queue()
        else:
            queue_3 = queue_out
        print(book.url)
        url = WEB_SETTINGS[web]['menu'].format(book.url)
        print(url)
        queue_1.put((web, url))
        print('开始创建目录线程')
        ReqThread(web, queue_1, queue_2, single=True, handle_response=self.down_handle(web)).start()
        print('目录线程创建完毕')
        # queue_2 返回的是章节目录
        AnalysisDown(web, queue_2, queue_3, book).start()
        print('下载线程创建完毕')

        return queue_3

    # 这里应该用线程池，但我没有用
    def createChapter(self, web, urls, queue_out):
        # Queue是线程安全的，不需要加锁
        queue_1 = Queue()
        t_list = []
        for i in range(3):
            t_list.append(self.run_fuck(web, queue_1, queue_out))
        for i, url in enumerate(urls):
            queue_1.put((i, url))

        for t in t_list:
            # t.is_over = True
            queue_1.put((web, 'over'))
        queue_1.put((web, 'over'))
        queue_1.put((web, 'over'))

    def run_fuck(self, web, queue_1, queue_out):
        t = ReqThread(web, queue_1, queue_out, single=True, handle_response=self.down_handle(web))
        t.start()
        return t


class AnalysisBase(object):
    def __init__(self, web):
        self.web = web
        print('web:', web)


# 解析下载任务，多线程
class AnalysisDown(threading.Thread, AnalysisBase):
    menu = []
    max_thread = 2
    thread_list = []
    chapter_handle = ChapterHandle

    def __init__(self, web, queue_menu, queue_chapter, book):
        threading.Thread.__init__(self)
        AnalysisBase.__init__(self, web)
        self.queue_menu = queue_menu
        self.queue_chapter = queue_chapter
        self.queue_t = Queue()
        self.book = book

    # 创建多个下载线程
    # queue_menu: 队列，从该队列中获取目录（一次性）
    # queue_chapter: 队列，一章一章地输出到该队列
    def creatDownThread(self):
        menu_len = len(self.menu)
        queue_in = Queue()
        self.setThreadList(queue_in)
        for i, menu_one in enumerate(self.menu):
            queue_in.put((i - menu_len, menu_one.url))
        for i in range(self.max_thread):
            queue_in.put((self.web, 'over'))

    # 创建线程池（假的线程池）
    def setThreadList(self, queue_in):
        for i in range(self.max_thread):
            rt = ReqThread(
                self.web, queue_in, self.queue_t,
                single=False, handle_response=self.chapter_handle(self.web))
            rt.start()
            self.thread_list.append(rt)

    def run(self):
        print(self.web)
        if not self.getMenu():
            self.queue_chapter.put(('404', self.menu))
            return
        self.creatDownThread()
        # 接收下载的章节
        self.getDown()
        # 保存
        self.save()
        self.queue_chapter.put(('over', '下载完成'))

    # 获取目录
    def getMenu(self):
        while 1:
            if self.queue_menu.empty():
                continue
            id, self.menu = self.queue_menu.get()
            if id == '404' or self.menu == '404':
                return False
            break
        # for m in self.menu:
        #     print(m.url, m.title)
        return True

    # 获取下载
    def getDown(self):
        count = len(self.menu)
        while count > 0:
            if self.queue_t.empty():
                continue
            id, content = self.queue_t.get()
            if content == 'over':
                continue
            self.menu[id].content = content
            self.queue_chapter.put((id, self.menu[id]))
            count -= 1

    def save(self):
        title = self.book.title
        author = self.book.author.replace('\n', '')
        print('作者：', author)
        genre = self.book.genre
        serial = self.book.serial
        word_n = self.book.word_n
        info = self.book.info_intact
        if not os.path.exists('txt/'):
            os.makedirs('txt/')
        with open('txt/《{}》by{}.txt'.format(title, author), 'w', encoding='utf-8') as f:
            print(self.web)
            f.write(Exemption.format(self.web))
            f.write('书名：{}\n作者：{}\n类型：{}\n连载：{}\n字数：{}\n简介：{}\n\n\n\n'.format(
                title, author, genre, serial, word_n, info
            ))
            sys.stdout.flush()
            for chapter in self.menu:
                print('写章节:{}'.format(chapter.title))
                f.write(chapter.title + '\n')
                f.write(chapter.content + '\n\n')


BaseHandle.req = Request
