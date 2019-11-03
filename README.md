#  CurrencyCrawlerChineseNovels

## 通用的小说爬取程序

如果你只是想使用这个软件，请阅读[这个](README_ABOUT.md)。

exe可执行程序下载

---



## 一、前言

爬虫应该不拘泥于爬指定的几个页面，它应该更通用、更智能。

我写了这个项目，它适用于大多数小说站点，只需要在配置文件中加入某个小说站点的一些必要的正则表达式或xpath表达式，就可以将该站点加入到程序中。

目前基本功能已经完成，但还剩余~~几个~~（很多）bug需要修改。



## 二、预览

搜索界面：



展示界面：



下载：





## 三、项目部署使用

### 1.环境搭建

1. python3(我使用的是python3.7)
2. PyQt5
3. pyinstaller（用来打包成exe文件，不是非必须的）

### 2.目录结构

```shell
xiaoshuo
|-crawler(爬虫模块)
| |-handle.py(提取爬取的数据)
| |-Middleware.py(处理请求头)
| |-Request.py(网络请求、创建网络请求)
| |-showData.py(渲染数据，因为一些原因并没有使用它)
|-image(项目资源)
| |-...
|-img(缓存图片)
| |-...
|-models(模型)
| |-book.py(书籍、章节类)
|-txt(下载的小说存放在这里)
| |-...
|-UI(窗口界面)
| |-...各个组件，懒得写了
|-main.py(入口)
|-settings.py(配置文件)
```

### 3.运行

```
python main.py
```



## 四、添加其他小说站点

见：[添加其他小说站点](README_ADDSITE)



## 五、打包为exe程序

 https://blog.csdn.net/zwyact/article/details/99778898 

python项目打包成exe有很多坑，踩了好多坑终于成功了。

首先我们安装pyinstaller:

```shell
pip3 install pyinstaller
# 速度慢的话可以使用镜像
# pip3 install pyinstaller -i https://mirrors.aliyun.com/pypi/simple
```

目录定位到项目目录下，执行：

```shell
pyinstaller -F -p D:\envs\py3_qt\Lib main.py
# -D : 打包成多个文件
# -F : 打包成一个单独的文件
# -p : 指定第三方包的目录，如果你用的是虚拟环境，那么这个是必须的。
```

pyinstaller 还有其他的很多参数，可以自行百度。

执行后，项目目录下会多出两个文件夹： build/ 、 dist/ ，和一个文件：main.spec。

将它们复制到一个空文件夹，进入dist目录，会看到main.exe。

这时候先在该目录下创建三个文件夹：txt/、image/、img/。

我不记得我又没有在代码中写自动创建这三个目录，你可以试一下看看。

然后双击main.exe，就可以打开了，打开的过程可能有些慢。

然后发到另一台电脑，看看能不能正常运行。



---

这里不得不说一下这个很坑的坑：

```python
import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
```

这是main.py文件的前三行，你可以试试去掉它，然后打包。

你就会发现在自己电脑上仍然可以用，但到了另一台电脑就用不了。



详细使用说明见：[使用说明](README_ABOUT.md)



## 六、关于作者

TigerWang

GitHub: https://github.com/VacantHusky 

邮箱：conan1015@foxmail.com

个人博客：www.hbmu.xyz



如果你有好的建议，欢迎联系我。



## 七、免责声明

~~你们随便用，反正侵了权别找我。~~

本项目遵循那个什么GNU协议，好像是说除了商用和闭源，其他的可以随便。

**请尊重别人的版权，此项目仅用于学习，对于下载的txt文件，请在24小时内删除。**

**禁止大范围传播，禁止商用。**


