IS_QT5 = True

# 小说站点名字，如果使用中文出现异常请改为英文字母
# 名字不要起的太长
# 名字必须和 WEB_SETTINGS 中的一致
# 必须加入到该列表才会生效
WEB_NAME = [
    '纵横网','3G书城','易读网',
]

WEB_SETTINGS = {
    '纵横网': {
        'code': 'utf-8',
        'host': 'http://search.zongheng.com/',  # host
        'search': 'http://search.zongheng.com/s?keyword={}',  # 搜索链接
        'menu': 'http://book.zongheng.com/showchapter/{}.html',  # 目录连接
        'search_re': {
            'url':'<h2 class="tit"><a href="http://book.zongheng.com/book/(.*?).html"',
        },  # 搜索结果的re
        'search_xpath': {
            # 'url': '//h2[@class="tit"]/a/@href', # 这个实际上是book_id
            'image': '//div[@class="imgbox fl se-result-book"]/a/img/@src',
            'title': '//h2[@class="tit"]',
            'author': '//div[@class="fl se-result-infos"]/div[@class="bookinfo"]/a[1]',
            'genre': '//div[@class="fl se-result-infos"]/div[@class="bookinfo"]/a[2]',
            'serial': '//div[@class="fl se-result-infos"]/div[@class="bookinfo"]/span[1]',
            'word_n': '//div[@class="fl se-result-infos"]/div[@class="bookinfo"]/span[2]',
            'info': '//div[@class="fl se-result-infos"]/p',
        },
        'chapter_xpath': {
            'url': '//ul[@class="chapter-list clearfix"]/li/a/@href',
            'title': '//ul[@class="chapter-list clearfix"]/li/a',
            'content': '//div[@class="content"]',
        },
    },
    '3G书城': {
        'code': 'utf-8',
        'host': 'http://www.3gsc.com.cn/',  # host
        'search': 'http://www.3gsc.com.cn/search/index/show/pic?search_key={}',  # 搜索链接
        'menu': 'http://www.3gsc.com.cn/bookreader/{}',  # 目录连接
        'search_re': {
            'url': '<p><a href="/book/(.*?)" class="Article"',
            'word_n': '总字数：(.*?)<br>',
        },  # 搜索结果的re
        'search_xpath': {
            'image': '//a[@class="recommended-reading-book"]/img/@src',
            'title': '//a[@class="Article"]',
            'author': '//div[@class="Explain"]/p[1]/a[2]/text()',
            'genre': '//div[@class="Explain"]/p[1]/a[3]/text()',
            'serial': '//div[@class="Explain"]/p[4]',
            'info': '//div[@class="Explain"]/p[2]',
        },
        'chapter_re': {
            '空':''
        },
        'chapter_xpath': {
            'url': '//div[@class="menu-area"]/p[1]/a/@href',
            'title': '//div[@class="menu-area"]/p[1]/a/@title',
            'content': '//div[@class="menu-area"]',
        },
    },
    '易读网': {
        'code': 'gb2312',
        'host': 'https://www.yiduks.com/',  # host
        'search_method': 'post',
        'search_form_data': {'key':None},
        'search_form_search_key': 'key',
        'search': 'https://www.yiduks.com/search.php',  # 搜索链接
        'menu': 'https://www.yiduks.com/{}.html',  # 目录连接
        'search_re': {
            'url': "<a href='(.*?)\.html' target='_blank' >",
            'word_n': "<a href='.*?\.html' target='(.*?)' >",
            'image': '',
            'title': "<a href='.*?' target='_blank' >(.*?)</A>",
            'author': '<TD Class=New>(.*?)</TD>',
            'genre': "<a href='.*?\.html' target='(.*?)' >",
            'serial': "<a href='.*?\.html' target='(.*?)' >",
            'info': "<a href='.*?\.html' target='(.*?)' >",
        },  # 搜索结果的re
        'search_xpath': {
            '空':''
        },
        'chapter_re': {
            '空':''
        },
        'chapter_xpath': {
            'url': '//div[@class="menu-area"]/p[1]/a/@href',
            'title': '//div[@class="menu-area"]/p[1]/a/@title',
            'content': '//div[@class="menu-area"]',
        },
    },
}




Exemption = '声明：\n该小说爬取自{}，可能会侵害他人的权益，请在下载后24小时内删除。\nby:www.hbmu.xyz\n\n'
