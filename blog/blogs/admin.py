from blog.blogs.models import Category
from blog.blogs.models import Comment
from blog.blogs.models import Post
from blog.blogs.models import Tag
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "created_at")

    list_filter = ("status", "category", "created_at", "author")

    search_fields = ("title", "body")

    prepopulated_fields = {"slug": ("title",)}

    inlines = [CommentInline]

    filter_horizontal = ("tags",)
