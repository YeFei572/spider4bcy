import requests
from bs4 import BeautifulSoup
import urllib

class getHtmlUrl(object):

    def __init__(self):
        self.server = "http://www.audio699.com/book/293/"
        self.resourceUrl = []
        self.totalPage = 2
        self.path = 'd:/xmly'

    def getResourceUrl(self):
        headers = {   
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
        } 
        for i in range(self.totalPage):
            req = requests.get(url=self.server + '122.html', headers=headers)
            bf = BeautifulSoup(req.text, "html.parser")
            audios = bf.find('source')
            self.resourceUrl.append(audios.get('src'))

    def downloadM4a(self):
        no = 0
        for i in self.resourceUrl:
            no = no + 1
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
            try:
                req = urllib.request.Request(i, headers=headers)
                data = urllib.request.urlopen(req).read()
                with open('D/XiMaLaya/' + '1.m4a', 'wb') as f:
                    f.write(data)
                    f.close()
            except Exception as e:
                print(str(e))
            # try:
            #     print(i)
            #     urllib.request.urlretrieve(i, 'D:\XiMaLaya\\'+str(i+'.m4a'))
            #     print(str(i), '...【下载成功】')
            # except:
            #     print(i + '下载失败了')



if __name__ == "__main__":
    dl = getHtmlUrl()
    dl.getResourceUrl()
    dl.downloadM4a()