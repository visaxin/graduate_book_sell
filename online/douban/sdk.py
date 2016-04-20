#!/usr/bin/env python
# encoding: utf-8


from douban_client import DoubanClient
from ruamel import yaml
import logging
import threading

API_KEY = ''
API_SECRET = ''

SCOPE = 'douban_basic_common,shuo_basic_r,shuo_basic_w,book_basic_r'

client = DoubanClient(API_KEY, API_SECRET, '', SCOPE)
client.auth_with_password('', '')

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

