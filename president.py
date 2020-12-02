import requests
from bs4 import BeautifulSoup
import pymysql


class write2Mysql(object):
    def __init__(self):
        self.server = 'http://wisdom.ichinaceo.com/news_list-id22-total378-p'
        self.urls = []
        self.titles = []
        self.createAts = []
        self.page = 1
        self.size = 11
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = 'keppel2016'
        self.db = 'test'
        self.table = 'president'

    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        password=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('mysql链接出错')


    def get_post_item(self):
        for num in range(self.page, self.size):
            singleUrl = self.server + str(num) + '.htm'
            print(singleUrl)
            resp = requests.get(singleUrl)
            bf = BeautifulSoup(resp.text, 'html.parser')
            texts = bf.find_all('ul', class_='maket_list')
            for item in texts:
                sonA = item.find_all('a')
                sonEm = item.find_all('em')
                for secondItem in sonA:
                    hrefStr = secondItem.get('href')
                    self.urls.append(hrefStr)
                    title = secondItem.string
                    self.titles.append(title[2:len(title)])
                for secondItem in sonEm:
                    self.createAts.append(secondItem.string[1:len(secondItem.string)-1])
                    print(secondItem)

    def save2Mysql(self):
        for index in range(len(self.urls)):
            insertSql = 'insert into article(title, url, create_at) values (\"%s\",\"%s\",\"%s\")'%(self.titles[index], self.urls[index], self.createAts[index])
            try:
                self.cursor.execute(insertSql)
                self.conn.commit()
            except:
                print('回滚')
                self.conn.rollback()
        self.conn.close()




if __name__ == '__main__':
    readHtml = write2Mysql()
    readHtml.connectMysql()
    readHtml.get_post_item()
    readHtml.save2Mysql()
#
# class Article:
#     '文章实体类'
#     def __init__(self, article, url, create_at, content):