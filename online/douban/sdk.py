#!/usr/bin/env python
# encoding: utf-8


from douban_client import DoubanClient
from ruamel import yaml
import logging
import threading

API_KEY = '04ab24bab939bb2f0e016e302bad318d'
API_SECRET = '71aae1c8bc723409'

SCOPE = 'douban_basic_common,shuo_basic_r,shuo_basic_w,book_basic_r'

client = DoubanClient(API_KEY, API_SECRET, 'http://rcis.cqupt.edu.cn/veidoo/DoubanTokenGetterServlet', SCOPE)
client.auth_with_password('visaxin', 'doubanspec')

logger = logging.getLogger(__file__)
con = threading.Condition()
sdk_count = 0

def getClient():
    return client


def getBookByIsbn(isbn):
    return client.book.isbn(isbn)


def getBookById(id):
    logger
    return client.book.get(id)


# for test
import json


def dgetBookByIsbn(isbn):
    d = json.dumps(
            {"rating": {"max": 10, "numRaters": 105924, "average": "8.8", "min": 0}, "subtitle": "“地球往事”三部曲之一",
             "author": ["刘慈欣"], "pubdate": "2008-1",
             "tags": [{"count": 36047, "name": "科幻", "title": "科幻"}, {"count": 27020, "name": "刘慈欣", "title": "刘慈欣"},
                      {"count": 16944, "name": "三体", "title": "三体"}, {"count": 11767, "name": "科幻小说", "title": "科幻小说"},
                      {"count": 11099, "name": "中国", "title": "中国"}, {"count": 9943, "name": "小说", "title": "小说"},
                      {"count": 8237, "name": "硬科幻", "title": "硬科幻"}, {"count": 6607, "name": "中国科幻", "title": "中国科幻"}],
             "origin_title": "", "image": "https://img1.doubanio.com\/mpic\/s2768378.jpg", "binding": "平装",
             "translator": [],
             "catalog": "1.科学边界\n2.台球\n3.射手和农场主\n4.三体、周文王、长夜\n5.叶文洁\n6.宇宙闪烁之一\n7.疯狂年代\n8.寂静的春天\n9.红岸之一\n10.宇宙闪烁之二\n11.大史\n12.三体、墨子、烈焰\n13.红岸之二\n14.红岸之三\n15.红岸之四\n16.三体、哥白尼、宇宙橄榄球、三日凌空\n17.三体问题\n18.三体、牛顿、冯·诺伊曼、秦始皇、三日连珠\n19.聚会\n20.三体、爱因斯坦、单摆、大撕裂\n21.三体、远征\n22.地球叛军\n23.红岸之五\n24.红岸之六\n25.叛乱\n26.雷志成、杨卫宁之死\n27.无人忏悔\n28.伊文斯\n29.第二红岸基地\n30.地球三体运动\n31.两个质子\n32.古筝行动\n33.监听员\n34.智子\n35.虫子\n36.尾声·遗址\n后记",
             "ebook_url": "http:\/\/read.douban.com\/ebook\/930946\/", "pages": "302",
             "images": {"small": "https://img1.doubanio.com\/spic\/s2768378.jpg",
                        "large": "https://img1.doubanio.com\/lpic\/s2768378.jpg",
                        "medium": "https://img1.doubanio.com\/mpic\/s2768378.jpg"},
             "alt": "https:\/\/book.douban.com\/subject\/2567698\/", "id": "2567698", "publisher": "重庆出版社",
             "isbn10": "7536692935", "isbn13": "9787536692930", "title": "三体",
             "url": "http:\/\/api.douban.com\/v2\/book\/2567698", "alt_title": "",
             "author_intro": "刘慈欣，祖籍河南，长于山西，中国科普作家协会会员，山西省作家协会会员，高级工程师。\n自1999年处女作《鲸歌》问世以来，刘慈欣已发表短篇科幻小说三十余篇、出版长篇科幻小说六部，并创下连续八年荣获中国科幻最高奖“银河奖”的纪录。他的长篇作品《三体》开创《科幻世界》月刊连载原创作品的先例，成为2006年度最受关注、最畅销的科幻小说。",
             "summary": "文化大革命如火如荼进行的同时。军方探寻外星文明的绝秘计划“红岸工程”取得了突破性进展。但在按下发射键的那一刻，历经劫难的叶文洁没有意识到，她彻底改变了人类的命运。地球文明向宇宙发出的第一声啼鸣，以太阳为中心，以光速向宇宙深处飞驰……\n四光年外，“三体文明”正苦苦挣扎——三颗无规则运行的太阳主导下的百余次毁灭与重生逼迫他们逃离母星。而恰在此时。他们接收到了地球发来的信息。在运用超技术锁死地球人的基础科学之后。三体人庞大的宇宙舰队开始向地球进发……\n人类的末日悄然来临。",
             "ebook_price": "5.99", "series": {"id": "38", "title": "科幻世界·中国科幻基石丛书"}, "price": "23.00"})

    return yaml.safe_load(d)


if __name__ == '__main__':
    print getBookById("1770782")