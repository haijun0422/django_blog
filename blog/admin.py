from django.contrib import admin
from .models import Article, Tag, Category


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'status', 'views', 'author', 'category']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


class CategoryAadmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAadmin)
admin.site.register(Tag, TagAdmin)
