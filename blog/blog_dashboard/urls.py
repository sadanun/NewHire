from django.urls import path

from .views import (
    category_create_view,
    category_delete_view,
    category_list_view,
    category_update_view,
    comment_create_view,
    comment_delete_view,
    post_create_view,
    post_delete_view,
    post_detail_view,
    post_list_view,
    post_update_view,
)

app_name = "blog_dashboard"
urlpatterns = [
    path("posts/", view=post_list_view, name="post-list"),
    path("post/new/", view=post_create_view, name="post-create"),
    path("post/<int:pk>/", view=post_detail_view, name="post-detail"),
    path("post/<int:pk>/edit/", view=post_update_view, name="post-update"),
    path("post/<int:pk>/delete/", view=post_delete_view, name="post-delete"),
    path("categories/", view=category_list_view, name="category-list"),
    path(
        "categories/<int:pk>/edit/", view=category_update_view, name="category-update"
    ),
    path("categories/new/", view=category_create_view, name="category-create"),
    path(
        "categories/<int:pk>/delete/", view=category_delete_view, name="category-delete"
    ),
    path(
        "comments/<int:comment_pk>/delete/",
        view=comment_delete_view,
        name="comment-delete",
    ),
    path(
        "posts/<int:post_pk>/comments/add/",
        view=comment_create_view,
        name="comment-create",
    ),
]
