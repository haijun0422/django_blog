from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
import datetime


class Article(models.Model):
    '''文章模型'''
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    title = models.CharField(max_length=50, unique=True, verbose_name='标题')
    slug = models.SlugField('slug', max_length=200, blank=True)
    body = RichTextField(verbose_name='正文')
    pub_time = models.DateTimeField(null=True, verbose_name='发布时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    mod_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    status = models.CharField(verbose_name='文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def save(self, *args, **kwargs):
        '''解决中文标题无法生成slug的问题,当id或slug为空时,利用slugify方法对标题解码,手动生成slug'''
        if not self.id or not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''通用视图所需要的get_abosolute_url方法'''
        return reverse('blog:article_detail', args=[str(self.pk), self.slug])

    def clean(self):
        '''重写clean方法，当文章状态为未发布时候, 不能有发布日期,　当文章状态为已发布,而发布日期为空时,发布时间改为当前时间'''
        if self.status == 'd' and self.pub_time is not None:
            self.pub_date = None
        # raise ValidationError('草稿没有发布日期. 发布日期已清空。')
        if self.status == 'p' and self.pub_time is None:
            self.pub_date = datetime.datetime.now()

    def viewed(self):
        '''浏览增加１'''
        self.views += 1
        self.save(update_fields=['views'])

    def published(self):
        '''把文章状态由草稿成发布'''
        self.status = 'p'
        self.pub_date = datetime.datetime.now()
        self.save(update_fields=['status', 'pub_date'])

    class Meta:
        db_table = 'b_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名', max_length=30, unique=True)
    slug = models.SlugField('slug', max_length=40)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True,
                                        on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug])

    def has_child(self):
        if self.category_set.all().count() > 0:
            return True

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'b_category'
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField('slug', max_length=40)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', args=[self.slug])

    def get_article_count(self):
        return Article.objects.filter(tags__slug=self.slug).count()

    class Meta:
        db_table = 'b_tag'
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name
