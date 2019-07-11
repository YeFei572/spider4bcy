# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import urllib
import time

class getHtmlUrl(object):

    def __init__(self):
        self.server = "http://www.audio699.com/book/293/"
        self.resourceUrl = []
        self.totalPage = 2
        self.chapter = 176
        self.path = 'd:/xmly'

    def getResourceUrl(self):
        headers = {         
            'Cookie': '__cfduid=dc979bcd1056648ca6668c353d5d8cb211562156949',
            'Host': 'www.audio699.com',
            'Referer': 'http://www.audio699.com/book/293.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        } 
        for i in range(self.totalPage):
            downloadUrl = self.server + str(i+self.chapter) + '.html'
            print(downloadUrl)
            req = requests.get(url=downloadUrl, headers=headers)
            bf = BeautifulSoup(req.text, "html.parser")
            audios = bf.find('source')
            self.resourceUrl.append(audios.get('src'))

    def downloadM4a(self):
        no = self.chapter - 1
        print('download begin...')
        for i in self.resourceUrl:
            print(i)
            no = no + 1
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}  
            try:
                req = urllib.request.Request(i, headers=headers)
                res = urllib.request.urlopen(req)
                print(res.getcode())
                print(res.info())
                path = r'D:\xia\\' + str(no) + '.m4a'
                data = res.read()
                print(path)
                with open(path, 'wb') as f:
                    f.write(data)
                    f.close()
                print(str(no) + '下载完毕, 下面开始沉睡10分钟.....')
                time.sleep(100)
                print('沉睡结束, 准备下载下一集....')
            except Exception as e:
                print(str(e))
        print('download over...')
        # 修改总集数为原来的+原来的及数量
        self.chapter = self.chapter + self.totalPage
        # 清空resourceUrl为空
        self.resourceUrl = []


if __name__ == "__main__":
    dl = getHtmlUrl()
    for i in range(10):
        dl.getResourceUrl()
        dl.downloadM4a()
        print('下一轮开始循环')
        time.sleep(3600)
        