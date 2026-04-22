from django.contrib import admin
from blogs.models import Category  , Tag, Post , Comment
from django.core.management import call_command
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','slug')

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'category', 'status', 'created_at')

    list_filter = ('status', 'category', 'created_at', 'author')

    search_fields = ('title', 'body')

    prepopulated_fields = {'slug': ('title',)}

    inlines = [CommentInline]

    filter_horizontal = ('tags',)
