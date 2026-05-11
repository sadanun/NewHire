from django.contrib import admin
from django.urls import path

from blog.blog_api.views import (
    all_blog_belongs_to_category,
    category_detail,
    category_list,
    comment_detail,
    comment_list,
    comment_list_in_post,
    post_detail,
    posts_list,
)

app_name = "blogs_api"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", view=posts_list, name="post-list"),
    path("posts/<int:pk>/", view=post_detail, name="post-detail"),
    path("categories/", view=category_list, name="category-list"),
    path("categories/<int:pk>/", view=category_detail, name="category-detail"),
    path("comments/", view=comment_list, name="comment-list"),
    path("comments/<int:pk>/", view=comment_detail, name="comment-detail"),
    path(
        "posts/<int:post_id>/comments/",
        view=comment_list_in_post,
        name="comment-list-in-post",
    ),
    path(
        "categories/<int:category_id>/posts/",
        view=all_blog_belongs_to_category,
        name="all-blog-belongs-to-category",
    ),
]
