#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, Error

import logging
import json


from douban import sdk
import redis

import models
import tag_views


TOP_ISBNS = 'top_isbns'
TOP_IDS = 'top_ids'
PV = 'pv_index'

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

logger = logging.getLogger(__name__)
# Create your views here.
def indexView(request):
    try:
        if request.user.is_authenticated():
            logger.info(request.user.get_full_name() + "visited!")
        books = tag_views.get_top_books_in_mongo(20)
    except Error as e:
        logger.error("error when get Books for index.html")
        render(request, 'error.html', {'error': e.message})
    return render(request, 'index.html', {'books': books, 'uu': request.user})


def loginView(request):
    if not request.user.is_authenticated():
        return render(request, "login.html", {})
    else:
        return indexView(request)


@login_required(login_url='/login/')
def manageView(request):
    return render(request, 'pages/index.html')


def loginReqest(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return render(request, "index.html", {'books': getBook(), 'uu': user})
        else:
            # Return a 'disabled account' error message
            render(request, 'login.html', {})
    else:
        return render(request, "error.html")


@login_required()
def logoutRequest(request):
    logout(request)
    return indexView(request)


def registerRequest(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    try:
        User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    except DatabaseError as e:
        return render(request, 'error.html', {'error', e.message})
    authenticate(username=username, password=password)
    return loginView(request)


def errorView(request):
    return render(request, "error.html", {})


def getBook():
    isbn = [9787533944407]
    # isbn = r.lrange(TOP_ISBNS, 0, -1)
    # ids = r.lrange(TOP_IDS, 0, -1)
    ids = []
    books = []
    if isbn:
        for _isbn in isbn:
            # first get in mysql
            _query_res = queryBookInMysqlByIsbn(_isbn)
            if _query_res:
                # round 9.2 => 9
                _query_res['rating']['average'] = round(float(_query_res['rating']['average']))
                books.append(_query_res)
                break
            # if not find in mysql . Get from douban
            b = sdk.getBookByIsbn(_isbn)
            saveBook(b)
            b['rating']['average'] = round(float(b['rating']['average']))
            books.append(b)
    if ids:
        for _id in ids:
            b = sdk.getBookById(_id)
            saveBook(b)
            b['rating']['average'] = round(float(b['rating']['average']))
            books.append(b)

    return books


def saveBook(book):
    rating = book['rating']
    if not book.has_key("series"):
        book['series'] = dict()
        book['series']['id'] = 1
        book['series']['title'] = ''
    try:
        b, created = models.Book.objects.get_or_create(
                id=int(book['id']), rating_max=int(rating['max']),
                rating_numraters=int(rating['numRaters']),
                rating_average=str(rating['average']),
                rating_min=int(rating['min']), subtitle=book['subtitle'], author=book['author'],
                pub_date=book['pubdate'], tags=str(book['tags']), origin_title=book['origin_title'],
                image=book['image'], binding=book['binding'], translator=book['translator'],
                catalog=book['catalog'], ebook_url=book['ebook_url'], pages=book['pages'],
                imgages=book['images'], alt=book['alt'], douban_id=book['id'], publisher=book['publisher'],
                isbn10=book['isbn10'], isbn13=book['isbn13'], title=book['title'], url=book['url'],
                alt_title=book['alt_title'], author_intro=book['author_intro'],
                ebook_price=book['ebook_price'], series_id=book['series']['id'],
                series_title=book['series']['title'], summary=book['summary'],
                price=book['price'], json_data=json.dumps(book))
        if created:
            print "Created in MySql!"

    except Error as e:
        print("Save to mysql fail!")
        print(e.message)


def queryBookInMysqlByIsbn(isbn):
    try:
        b = models.Book.objects.get(isbn13=isbn)
    except ObjectDoesNotExist:
        print("The Book  doesn't exist. Will curl from douban!")
        return None
    # return yaml.safe_load(serializers.serialize('json', b))
    # return yaml.safe_load(b.json_data)
    return json.loads(b.json_data)


def queryBookInMysqlById(id):
    try:
        b = models.Book.objects.get(id=id)
    except ObjectDoesNotExist:
        print("The Book  doesn't exist. Will curl from douban!")
        return None
    # return yaml.safe_load(b.json_data)
    return json.loads(b.json_data)


# update index books
def updateTopIsbns(isbns):
    if len(isbns) == 0:
        return
    if len(isbns) > 10:
        isbns = isbns[0:10]

    for isbn in isbns:
        r.rpush(TOP_ISBNS, isbn)


def validUser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    return user
