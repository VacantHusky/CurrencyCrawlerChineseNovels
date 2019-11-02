

class Chapter:
    id = -1
    url = ''
    title = ''
    content = ''


class Book:
    url = ''
    image = 'image/default.jpg'
    title = '书名'  # 书名
    author = '作者' # 作者
    genre = '类别'  # 类别
    serial = '连载' # 连载
    word_n = 0  # 字数
    info = '简介\n简介'   # 简介
    info_intact = ''
    save_path = ''  # 存储路径
    # 章节
    chapters = []

    def __str__(self):
        return '''
        《{}》 | {} | {} | {} | {} 
        {}
        '''.format(self.title,self.author,self.genre,self.serial,self.word_n,self.info)
