#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import url
import views
import tag_views

urlpatterns = [
    url(r'^$', views.indexView, name='index'),
    url(r'^login/$', views.loginView, name='login'),
    url(r'^error/', views.errorView, name='error'),
    url(r'^management/$', views.manageView, name='management'),

    url(r'^accounts/register/$', views.registerRequest, name='register'),
    url(r'^accounts/login/$', views.loginReqest, name='loginRequest'),
    url(r'^accounts/logout/$', views.logoutRequest, name='logoutRequest'),

    url(r'^tag/(?P<tag>\w+)/$', tag_views.searchTagViews, name='tag'),
    # url(r'^search/(?P<q>\w+)/$', tag_views.searchViews, name='q')
    url(r'^search/$', tag_views.searchViews, name='q'),
    url(r'^search/tag/$', tag_views.searchTagViewsForm, name='q_tag'),
    url(r'^book/detail/$', tag_views.detailView, name='detail'),

    url(r'^book/comment/$', tag_views.publish_comment_view, name='comment'),
    url(r'^book/comment/delete$', tag_views.delete_comment_view, name='delete_comment'),

    url(r'^cart/$', tag_views.cart_view, name='cart'),
    url(r'^cart/add$', tag_views.cart_add_view, name='add_cart'),
    url(r'cart/item/$',tag_views.item_delete_view,name='delete_in_cart'),
    url(r'order/$',tag_views.orderView,name='order')

]
