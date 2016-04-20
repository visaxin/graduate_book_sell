#!/usr/bin/env python
# encoding: utf-8
import logging
import threading

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django_ajax.decorators import ajax

import mongo
from common import util
from douban import sdk

# Get an instance of a logger
logger = logging.getLogger(__name__)

MONGO_DB = 'test'

DOUBAN_CLIENT = sdk.getClient()
mdb = mongo.getDB(MONGO_DB)


# sdk return a dict
# mongo return a cursor which type is a list
def tag_render(request, tag, result):
    if type(result) is dict:  #
        logger.debug("sdk")

        return render(request, 'tag.html', {'tag': tag, 'result': result['books'], 'uu': request.user})
    else:
        logger.debug("mongo")
        return render(request, 'tag.html', {'tag': tag, 'result': result[0]['books'], 'uu': request.user})


def updateSearchTagResultInMongo(result):
    for one_recode in result['books']:
        mdb.book.insert_one(one_recode)


# also using tag view
def searchTagViews(request, tag):
    # tag = request.GET.get('tag', '小说')
    mdb_search = {'tag': tag}
    mdb_res = mdb.search_tag.find(mdb_search)
    if mdb_res.count() > 0:
        logger.debug('Find in mongodb!')
        return tag_render(request, tag, mdb_res)
    else:
        logger.debug('I will using douban sdk!')
        result = DOUBAN_CLIENT.book.search(tag=tag)
        result['tag'] = tag

        t = threading.Thread(target=updateSearchTagResultInMongo, args=(result,))
        t.setDaemon(True)
        t.start()

        mdb.search_tag.insert_one(result)
        return tag_render(request, tag, result)

        # def search_render(request,q,result):
        # return render(request, 'tag.html', {'tag': q, 'result': result[0]['books'], 'uu': request.user})


def searchTagViewsForm(request):
    tag = request.GET.get('tag', '小说')
    mdb_search = {'tag': tag}
    mdb_res = mdb.search_tag.find(mdb_search)
    if mdb_res.count() > 0:
        logger.debug('Find in mongodb!')
        return tag_render(request, tag, mdb_res)
    else:
        logger.debug('I will using douban sdk!')
        result = DOUBAN_CLIENT.book.search(tag=tag)
        result['tag'] = tag

        t = threading.Thread(target=updateSearchTagResultInMongo, args=(result,))
        t.setDaemon(True)
        t.start()

        mdb.search_tag.insert_one(result)
        return tag_render(request, tag, result)

        # def search_render(request,q,result):
        # return render(request, 'tag.html', {'tag': q, 'result': result[0]['books'], 'uu': request.user})


def searchViews(request):
    q = request.GET.get('key_word', '图书')
    mdb_search = {'q': q}
    mdb_res = mdb.keyord_book.find(mdb_search)
    if mdb_res.count() > 0:
        logger.debug('Find in mongodb!')
        return tag_render(request, q, mdb_res)
    else:
        logger.debug('I will using douban sdk!')
        result = DOUBAN_CLIENT.book.search(q=q)
        result['q'] = q

        t = threading.Thread(target=updateSearchTagResultInMongo, args=(result,))
        t.setDaemon(True)
        t.start()

        mdb.keyword_book.insert_one(result)
        return tag_render(request, q, result)


def query_comments_by_book_id(_id):
    comment_search = {'book_id': _id}
    print "search booid=", _id, " comments"
    comment_res = mdb.comment.find(comment_search)
    if comment_res.count() > 0:
        return comment_res
    else:
        return


def get_book_by_id(_id):
    book_info = mdb.book.find_one({'id': _id})
    if book_info is None:
        book_info = mdb.book.find_one({"books.id": _id})
        if book_info is None:
            print("New sdk request for id:" + _id)
            sdk_result = sdk.getBookById(_id)
            mdb.book.insert_one(sdk_result)
            return sdk_result
    print "find in mongo when get_book_by_id"
    return book_info


def detailView(request):
    _id = str(request.GET.get('id', ''))

    book_info = get_book_by_id(_id)
    comments = query_comments_by_book_id(_id)
    return render(request, 'book_detail.html', {'book': book_info, 'uu': request.user, 'comments': comments})


@login_required()
def publish_comment_view(request):
    data = dict()
    data['content'] = request.POST.get('content', "no comment!")
    data['book_id'] = str(request.POST.get('book_id', ''))
    if not request.user.is_authenticated:
        data['publisher'] = request.user.get_full_name()
    else:
        data['publisher'] = "AnonymousUser"
    data['publish_date'] = util.mongo_now()
    mdb.comment.insert_one(data)
    print 'insert one comment: ', data
    return HttpResponse(data)


@login_required()
def delete_comment_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

            book_id = request.POST.get('book_id', '')
            publisher = request.POST.get('publisher', '')

            if publisher == '':
                publisher = request.user.get_full_name()
                print 'Admin handle: ', publisher
                print "delete: book+id=", book_id, "publisher=", publisher
                mdb.comment.delete_one({'book_id': book_id, 'publisher': publisher})
            else:
                if publisher != request.user.get_full_name():
                    return HttpResponse(status=401, content="You have no power!")
                else:
                    print "delete: book+id=", book_id, "publisher=", publisher
                    mdb.comment.delete_one({'book_id': book_id, 'publisher': publisher})
            return HttpResponse(status=200, content="Deleted!")
        else:
            return HttpResponse(status=401, content="You have no power!")


@login_required()
def cart_add_view(request):
    if request.user.is_authenticated():
        cart = dict()
        cart['book_id'] = request.POST.get('book_id', '')
        cart['book_quantity'] = int(request.POST.get('book_quantity', '1'))
        cart['cart_owner'] = request.user.username

        mfilter = {'cart_owner': cart['cart_owner'], 'book_id': cart['book_id']}
        mres = mdb.cart.find(mfilter)

        # book_ids = []
        # for m in mres:
        #     book_ids.append(m['book_id'])

        book_info = get_book_by_id(cart['book_id'])
        cart['book_price'] = book_info['price']
        cart['book_title'] = book_info['title']
        if mres.count() > 0:
            mdb.cart.update_one(mfilter, {'$set':
                                              {'book_quantity': int(mres[0]['book_quantity']) + cart['book_quantity']}
                                          })
        else:
            mdb.cart.insert_one(cart)
        print request.user.username
        user_cart_info = mdb.cart.find({'cart_owner': request.user.username})
        # books_info = get_book_by_ids(book_ids)

        return render(request, 'cart.html', {'carts': user_cart_info})
    else:
        render(request, 'login.html', {})


@ajax
@login_required()
def item_delete_view(request):
    if request.user.is_authenticated():
        cart = dict()
        cart['book_id'] = request.POST.get('item', '')
        cart['cart_owner'] = request.POST.get('owner', '')
        mfilter = {'cart_owner': cart['cart_owner'], 'book_id': cart['book_id']}
        mres = mdb.cart.delete_one(mfilter)

        return {}
    else:
        render(request, 'login.html', {})


def cart_view(request):
    if request.user.is_authenticated():
        user_cart_info = mdb.cart.find({'cart_owner': request.user.username})
        return render(request, 'cart.html', {'carts': user_cart_info})
    else:
        return render(request, 'cart.html', {'carts': {}})


def get_book_by_ids(_ids):
    books_info = []
    for _id in _ids:
        books_info.append(mdb.book.find_one({"id": _id}))
    return books_info


def get_top_books_in_mongo(top):
    if type(top) != "int":
        return mdb.book.find().limit(10)
    else:
        return mdb.book.fin().limit(top)


@ajax
def orderView(request):
    if request.user.is_authenticated():
        order = dict()
        order['itmes'] = list(mdb.cart.find({'cart_owner': request.user.username}))
        order['owner'] = request.user.username
        order['time'] = util.mongo_now()
        order['address'] = "default addressß"
        mdb.order.insert_one(order)
        return "success!"
    return "failed!"
