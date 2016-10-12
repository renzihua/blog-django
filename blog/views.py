# coding:utf-8

import logging
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage,InvalidPage,PageNotAnInteger
from .models import *
from django.db.models import Count
from .forms import CommentForm,LoginForm,RegForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password

logger = logging.getLogger("blog.views")

# Create your views here.

#配置全局变量，传递给每一个页面
def global_settings(request):

    #全局配置信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    SINA_WEIBO = settings.SINA_WEIBO
    SITE_URL = "http://www.baidu.com"

    # 目录
    category_list = Category.objects.all()[0:2]

    # 文章归档
    archives = Article.objects.distinct_date()

    cid = 1

    # 评论数最多的文章的排序
    comment_list = Comment.objects.values('article').annotate(comment_count = Count('content')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_list]

    return locals()

def home(request):
    try:
        # 获取最新文章,并提供分页
        articals = Article.objects.all()
        articals = paginator(request,articals)

    except Exception as e:
        logger.error(e)

    return render(request,"index.html",locals())

# 文章归档
def archive(request):
    try:
        # 得到文章归档的年和月
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)

        # 获取符合年和月的文章
        articals = Article.objects.filter(date_publish__icontains = year + '-' + month)

        # 设置分页
        articals = paginator(request,articals)

    except Exception as e:
        logger.error(e)

    return render(request,"archive.html",locals())

# 文章详情页
def article(request,id):
    try:
        article = Article.objects.get(pk=id)

        # 查找出所有的评论
        comment_list = get_comment(request,id)

        # 评论的form
        comment_form = CommentForm({
            'author':request.user.username,
            'email':request.user.email,
            'url':request.user.url,
            'article':id
        }if request.user.is_authenticated()else{'article':id})

    except Article.DoesNotExist:
        return render(request,"failure.html",{"reason":"此文章不存在"})

    return render(request,"article.html",locals())


# 创建分页器
def paginator(request,list):
    # 创建分页器
    paginator = Paginator(list, 2)

    # 获取分页内的文章
    try:
        page_index = int(request.GET.get('page', 1))
        result_list = paginator.page(page_index)
    # 用户返回的错误请求时，将系统返回到第一页
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        result_list = paginator.page(1)


    return result_list

# 分类
def category(request):
    return render(request, "index.html", locals())

# 评论功能
def get_comment(request,id):
    try:

        # 查询这篇文章

        # 查询文章下的所有评论
        comment_list = Comment.objects.filter(article__id = id).order_by('-date_publish')

        # 筛选出所有的父评论
        parent_comment_list = []
        # parent_comment = [comment for comment in comment_list if not comment.pid]
        for comment in comment_list:
            if not comment.pid:
                parent_comment_list.append(comment)
                if not hasattr(comment, "children_comment"):
                    setattr(comment, "children_comment", [])

        # 筛选出所有的子评论,并将其绑定到对应的父评论上
        for comment in comment_list:
            if comment.pid:
                for parent_comment in parent_comment_list:
                    if comment.pid == parent_comment:
                        parent_comment.children_comment.append(comment)

    # 异常信息
    except Exception as e:
        logger.error(e)

    # 返回信息
    return parent_comment_list

# 添加评论
def comment_post(request):
    try:
        # 获取这篇文章

        # 获取评论所在的post
        comment_form = CommentForm(request.POST)

        # 创建一个评论
        if comment_form.is_valid():

            comment = Comment.objects.create(
                content = comment_form.cleaned_data['comment'],
                username = comment_form.cleaned_data['author'],
                email = comment_form.cleaned_data['email'],
                url = comment_form.cleaned_data['url'],
                article_id = comment_form.cleaned_data['article']
            )

            comment.save()
        else:
            return render(request,"failure.html",{"reason":"数据填写有误"})

    except Exception as e:
        logger.error(e)

    return redirect(request.META['HTTP_REFERER'])

def do_login(request):
    try:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username = username,password = password)

                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request,user)
                    return redirect(request.POST.get('source_url'))
                else:
                    return render(request, "failure.html", {"reason": "登陆验证失败"})
            else:
                return render(request,"failure.html",login_form.errors)
        else:
            login_form = LoginForm()

    except Exception as e:
        logger.error(e)

    return render(request,"login.html",locals())

def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)

    return redirect(request.META["HTTP_REFERER"])

def reg(request):
    try:
        if request.method == "POST":
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(
                    username = reg_form.cleaned_data['username'],
                    email = reg_form.cleaned_data['email'],
                    url = reg_form.cleaned_data['url'],
                    password = make_password(reg_form.cleaned_data['password'])
                )

                user.save()

                # 登陆blog
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                #返回原网页
                return redirect(request.POST.get("source_url"))
            else:
                return render(request,"failure.html",{"reason":"注册失败"})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)

    return render(request,"reg.html",locals())



