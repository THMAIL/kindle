#*-*coding=utf-8*-*
import requests
from bs4 import BeautifulSoup
import os

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  new folder...  ---"
        print "---  OK  ---"
    else:
        print "---  There is this folder!  ---"

def printf(str):
        print('*' * 50)
        print(str)
        print('*' * 50)

class spider:
    url = ""
    headers = {}
    listSet = set()   #去重
    titleSet = set()
    
    def __init__(self, url = r'http://heibaimanhua.com/weimanhua/kbmh', headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}):
        self.url = url
        self.headers = headers
    
    #获取所有漫画列表页并解析，存入listSet
    def grabList(self):
        resp = requests.get(self.url, headers = self.headers)
        soup = BeautifulSoup(resp.text, features="html.parser")
        #筛去下载过的
        lastFinish = ""
        with open('finish.txt', 'r') as finish:
            lastFinish = finish.readline()
        #pageList = soup.select('div[class="content-box posts-image-box"]')
        pageList = soup.select("div.content-box")
        print(len(pageList))
        #print lastFinish
        #print lastFinish.replace('\n','')
        lastFinish = lastFinish.replace('\n','')
        for page in pageList:
            #print(page.select('a[href^="http://heibaimanhua.com/weimanhua/kbmh/"]')[0]['href'])
            href = page.select('a[href^="http://heibaimanhua.com/weimanhua/kbmh/"]')[0]['href']
            print href
            if(href == lastFinish):
                with open('finish.txt', 'w') as finish:
                    finish.write(pageList[0].select('a[href^="http://heibaimanhua.com/weimanhua/kbmh/"]')[0]['href'])
                printf('解析目录完成1')
                return 0
            self.listSet.add(href)
        with open('finish.txt', 'w') as finish:
            finish.write(pageList[0].select('a[href^="http://heibaimanhua.com/weimanhua/kbmh/"]')[0]['href'])
        printf('解析目录完成2')
    
    #下载漫画
    def getComicToFolder(self, url):
        #请求页面
        resp = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(resp.text, features="html.parser")
        #获取标题
        title = soup.h1.text
        self.titleSet.add(title)
        printf('正在下载' + title.encode('utf-8'))
        mkdir(title)
        #解析多页
        pageLinks = soup.select('div[class="page-links"]')
        self.getPic(url, title)
        if(len(pageLinks)):#该漫画有多页
            pageLinks = pageLinks[0].select('a')
            for pageNum in range(0, len(pageLinks)-2):
                self.getPic(pageLinks[pageNum]['href'], title)

    #下载一页漫画，供getComicToFolder()调用
    def getPic(self, url, name):
        #请求页面
        resp = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(resp.text, features="html.parser")
        listOfImage = soup.select('div[class="post-image"]')
        #获取目标路径下最大图片序号
        files= os.listdir(name)
        temp = 0
        for file in files:
            file = file.replace('.jpg', '')
            if(int(file) > temp):
                temp = int(file)
        for image in listOfImage:
            res = requests.get(image.img['src'], headers = self.headers)
            if res.status_code == 200:
                temp += 1
                tempFile = open('./' + name + '/' + str(temp) + '.jpg', 'wb')
                tempFile.write(res.content)
                tempFile.close()
                
    def start(self):
        self.grabList()
        print '待下载：' + str(len(self.listSet))
        for task in self.listSet:
            print task
        for commic in self.listSet:
            self.getComicToFolder(commic)

if __name__ == '__main__':
    test = spider()
    #test.getPic(r'http://heibaimanhua.com/weimanhua/kbmh/151433.html', '寄生人类')
    #test.getComicToFolder(r'http://heibaimanhua.com/weimanhua/kbmh/151471.html')
    test.start()
