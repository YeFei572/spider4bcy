#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json

import requests
import xlwt as xlwt
from bs4 import BeautifulSoup


class downloader(object):

    def __init__(self):
        self.server = 'https://bcy.net'
        self.target = 'https://bcy.net/coser'
        self.top = 'https://bcy.net/coser/toppost100?type=lastday'
        self.commentUrl = 'https://bcy.net/apiv3/cmt/reply/list?page=1&sort=hot&item_id='
        self.postIds = []
        self.urls = []
        self.nums = 0
        self.imageUrls = []

    def get_post_id(self):
        start = '2019-03-09'
        end = '2019-03-10'
        startAt = datetime.datetime.strptime(start, '%Y-%m-%d')
        endAt = datetime.datetime.strptime(end, '%Y-%m-%d')
        while startAt<endAt:
            startAt += datetime.timedelta(days=1)
            date = startAt.strftime('%Y%m%d')
            req = requests.get(url=self.top+'&date='+date)
            bf = BeautifulSoup(req.text)
            texts = bf.find_all('a', class_='db posr ovf')
            for each in texts:
                print(each)
                self.urls.append(each.get('href').split('/', -1)[-1])
                print(each.get('href').split('/', -1)[-1])

    def get_comment_detail(self):
        excel_line = 0
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        for each in self.urls:
            req = requests.get(url=self.commentUrl+each)
            # result = req.json()
            num = 0
            result = json.loads(req.content.decode())
            while len(result['data'].get('data')) > num:
                uname = result.get('data').get('data')[num].get('uname')
                cont = result.get('data').get('data')[num].get('content')
                sheet.write(excel_line, 0, uname)  # 第0行第一列写入内容
                sheet.write(excel_line, 2, cont)  # 第0行第一列写入内容
                excel_line = excel_line+1
                num = num+1
            print(req.json())
            wbk.save('test1.xls')

    def get_download_url(self):
        req = requests.get(url=self.target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('a', class_='db posr ovf')
        for each in texts:
            self.urls.append(each.get('href').split('/', -1)[-1])
        print(texts)
        return texts


if __name__=="__main__":
    dl = downloader()
    # dl.get_download_url()
    dl.get_post_id()
    # dl.get_comment_detail()