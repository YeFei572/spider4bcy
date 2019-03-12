import datetime
import os
import re

import requests
from bs4 import BeautifulSoup


class downloader(object):

    def __init__(self):
        self.path = 'd:/bcy'
        self.serverUrl = 'https://bcy.net'
        self.targetUrl = 'https://bcy.net/coser/toppost100?type=lastday'
        self.detailUrl = 'https://bcy.net/item/detail/'  # 帖子详情+帖子id
        self.postIds = []
        self.images = []

    def get_post_id(self):
        start = '2019-03-09'
        end = '2019-03-10'
        start_at = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_at = datetime.datetime.strptime(end, '%Y-%m-%d')
        while start_at < end_at:
            start_at += datetime.timedelta(days=1)
            date = start_at.strftime('%Y%m%d')
            req = requests.get(url=self.targetUrl + '&date=' + date)
            bf = BeautifulSoup(req.text)
            texts = bf.find_all('a', class_='db posr ovf')
            for each in texts:
                self.postIds.append(each.get('href').split('/', -1)[-1])

    def get_img_url(self):

        # 粉丝可见标记
        fans_tag = False

        for postId in self.postIds:
            req = requests.get(url=self.detailUrl+postId)
            bf = BeautifulSoup(req.text)

            # 作者名称
            name = bf.find(class_='user-name').get_text()
            html_script = bf.find_all('script')
            aim_script = ''
            for i in html_script:
                if 'window.__ssr_data' in i.text:
                    aim_script = i
                    break

            url_list = []
            aim_script = aim_script.text.split(",")
            for i in aim_script:
                if 'original_path' in i:
                    i = re.sub(r".*https", "", i)
                    i = re.sub(r"\\\\u002F", "/", i)
                    i = "https" + re.sub(r"\\\"}||]", "", i)
                    url_list.append(i)
                elif '粉丝可见' in i:
                    fans_tag = True
                    break
            if not (url_list or fans_tag):
                return None

            path = self.path + name + '_' + postId
            if not os.path.exists(path):
                # 如果不存在则创建目录
                os.makedirs(path)
                print(name + '_' + postId + " 作品开始保存")
            else:
                # 如果目录存在则不创建，并提示目录已存在
                print(name + '_' + postId + " 已保存作品，无需重复保存")
                print("_________________________________")
                return None

            if fans_tag:
                fp = open(path + '/粉丝可见.txt ', 'w')
                fp.close()
            else:
                j = 1
                for i in url_list:
                    fp = open(path + '/' + str(j) + '.jpg ', 'wb+')
                    fp.write(requests.get(i, timeout=30).content)
                    fp.close()
                    j += 1

            print("保存完成")
            print("_________________________________")

if __name__ == '__main__':
    dl = downloader()
    dl.get_post_id()
    dl.get_img_url()
