#!/usr/bin/env python
# encoding: utf-8

from pymongo import MongoClient
from bson.binary import Binary
import pickle
client = MongoClient()

def getClient():
    return client


def getDB(db):
    return client[db]


