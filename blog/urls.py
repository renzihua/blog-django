# coding:utf-8

from django.conf.urls import url
from blog.views import *

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r"^archive/",archive,name="archive"),
    url(r"^category/",category,name="category"),
    url(r"^article/(?P<id>[0-9]+)$",article,name="article"),
    url(r"^comment_post/$",comment_post,name="comment_post"),
    url(r"^login/$",do_login,name="login"),
    url(r"^logout/$",do_logout,name="logout"),
    url(r"^reg/$",reg,name="reg"), # 注册
    ]

