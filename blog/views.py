from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy

from .models import Article, Tag, Category
from .forms import ArticleForm


# Create your views here.

class ArticleListView(ListView):
    '''文章列表,不需要登录'''
    template_name = 'article_list.html'
    paginate_by = 3  # 指定对获取到的模型列表进行分页，这里每页3个数据

    def get_queryset(self):
        '''重写get_queryset()方法,展示所有发布文章。在之前，ListView默认会返回Model.objects.all()'''
        articles = Article.objects.filter(status='p').order_by('-pub_date')  # 获取已发布文章,并按发布时间倒序
        return articles


@method_decorator(login_required,
                  name='dispatch')  # 在类视图中使用为函数视图准备的装饰器时，不能直接添加装饰器，需要使用method_decorator将其转换为适用于类视图方法的装饰器。使用name参数指明被装饰的方法
class PublishedArticleListView(ListView):
    template_name = 'published_article_list.html'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user  # 获取当前用户
        articles = Article.objects.filter(author=user).filter(status='p').order_by('-pub_date')  # 获取当前用户发布的文章
        return articles


@method_decorator(login_required, name='dispatch')
class ArticleDraftListView(ListView):
    '''展示草稿列表'''
    template_name = 'article_draft_list.html'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        articles = Article.objects.filter(author=user).filter(status='d').order_by('-pub_date')
        return articles


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)  # 调用父类方法
        obj.viewed()
        return obj


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_update_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj


@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj


@login_required()
def article_publish(request, pk, slug1):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    article.published()
    return redirect(reverse("blog:article_detail", args=[str(pk), slug1]))
