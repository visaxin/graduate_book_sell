#!/usr/bin/env python
# encoding: utf-8
import time
import datetime

def now():
    return time.asctime(time.localtime(time.time()))

def mongo_now():
    return datetime.datetime.utcnow()