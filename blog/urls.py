# -*- coding: utf-8 -*-
# @Time    : 19-1-11 下午1:57
# @Author  : Nick
# @Email   : haijun0422@126.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, re_path
from . import views
app_name = 'blog'
urlpatterns = [
    # 所有文章列表
    path('', views.ArticleListView.as_view(), name='article_list'),
    # 展示文章详情
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    # 草稿箱
    path('draft/', views.ArticleDraftListView.as_view(), name='article_draft_list'),
    # 已发表文章列表(含编辑)
    path('admin/', views.PublishedArticleListView.as_view(), name='published_article_list'),
    # 更新文章-
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/update/$', views.ArticleUpdateView.as_view(),
            name='article_update'),
    # 创建文章
    re_path(r'^article/create/$', views.ArticleCreateView.as_view(), name='article_create'),
    # 发表文章登录
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/publish/$', views.article_publish, name='article_publish'),
    # 删除文章
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/delete$', views.ArticleDeleteView.as_view(),
            name='article_delete'),
    # 展示类别列表
    # re_path(r'^category/$', views.CategoryListView.as_view(), name='category_list'),
    # # 展示类别详情
    # re_path(r'^category/(?P<slug>[-\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    # # 展示Tag详情
    # re_path(r'^tags/(?P<slug>[-\w]+)/$', views.TagDetailView.as_view(), name='tag_detail'),
    # # 搜索文章
    # re_path(r'^search/$', views.article_search, name='article_search'),
]
