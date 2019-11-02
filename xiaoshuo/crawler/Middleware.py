from fake_useragent import UserAgent
from urllib.parse import splittype, splithost

from settings import WEB_SETTINGS

base_heard = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.baidu.com',
    'Referer': 'https://www.baidu.com/',
}

base_image_heard = {

}

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def __init__(self):
        super().__init__()
        self.ua = UserAgent()

    def read_heard(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, headers, web, url):
        for key, value in base_heard.items():
            headers[key] = value
        headers['User-Agent'] = self.ua.random
        proto, rest = splittype(url)
        host, rest = splithost(rest)
        # host = WEB_SETTINGS[web]['host']
        if host[-1]=='/':
            host = host.split('/')[-2]
        else:
            host = host.split('/')[-1]
        headers['Host'] = host

        headers['Referer'] = WEB_SETTINGS[web]['search'].format('')
        headers['Upgrade-Insecure-Requests'] = '1'


class CookiesMiddleware(object):
    """ 换Cookie """
    cookie = {
        'platform': 'pc',
        'ss': '367701188698225489',
        'bs': '%s',
        'RNLBSERVERID': 'ded6699',
        'FastPopSessionRequestNumber': '1',
        'FPSRN': '1',
        'performance_timing': 'home',
        'RNKEY': '40859743*68067497:1190152786:3363277230:1'
    }

    def process_request(self, request, spider):
        bs = ''
        for i in range(32):
            bs += chr(random.randint(97, 122))
        _cookie = json.dumps(self.cookie) % bs
        request.cookies = json.loads(_cookie)
