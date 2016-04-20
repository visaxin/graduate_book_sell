#!/usr/bin/env python
# encoding: utf-8
import urllib2

ISBN_URL = 'https://api.douban.com/v2/book/isbn/'

def apiRequest(url):
    res = urllib2.urlopen(url)
    # result = res.read().decode('utf-8')  result's type is unicode
    result = res.read()  # result's type is str
