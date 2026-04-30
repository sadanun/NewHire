from django.urls import path
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class DashboardConfig(OscarDashboardConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog.blog_dashboard"
    label = "blog_dashboard"

    def ready(self):
        super().ready()
        self.post_list_view = get_class("blog_dashboard.views", "PostListView", "blog")
        self.post_create_view = get_class(
            "blog_dashboard.views", "PostCreateView", "blog"
        )
        self.post_detail_view = get_class(
            "blog_dashboard.views", "PostDetailView", "blog"
        )
        self.post_update_view = get_class(
            "blog_dashboard.views", "PostUpdateView", "blog"
        )
        self.post_delete_view = get_class(
            "blog_dashboard.views", "PostDeleteView", "blog"
        )
        self.category_list_view = get_class(
            "blog_dashboard.views", "CategoryListView", "blog"
        )
        self.category_create_view = get_class(
            "blog_dashboard.views", "CategoryCreateView", "blog"
        )
        self.category_update_view = get_class(
            "blog_dashboard.views", "CategoryUpdateView", "blog"
        )
        self.category_delete_view = get_class(
            "blog_dashboard.views", "CategoryDeleteView", "blog"
        )
        self.comment_delete_view = get_class(
            "blog_dashboard.views", "CommentDeleteView", "blog"
        )
        self.comment_create_view = get_class(
            "blog_dashboard.views", "CommentCreateView", "blog"
        )

    def get_urls(self):
        urls = [
            path("posts/", self.post_list_view.as_view(), name="post-list"),
            path("post/new/", self.post_create_view.as_view(), name="post-create"),
            path("post/<int:pk>/", self.post_detail_view.as_view(), name="post-detail"),
            path(
                "post/<int:pk>/edit/",
                self.post_update_view.as_view(),
                name="post-update",
            ),
            path(
                "post/<int:pk>/delete/",
                self.post_delete_view.as_view(),
                name="post-delete",
            ),
            path(
                "categories/", self.category_list_view.as_view(), name="category-list"
            ),
            path(
                "categories/<int:pk>/edit/",
                self.category_update_view.as_view(),
                name="category-update",
            ),
            path(
                "categories/new/",
                self.category_create_view.as_view(),
                name="category-create",
            ),
            path(
                "categories/<int:pk>/delete/",
                self.category_delete_view.as_view(),
                name="category-delete",
            ),
            path(
                "comments/<int:comment_pk>/delete/",
                self.comment_delete_view.as_view(),
                name="comment-delete",
            ),
            path(
                "posts/<int:post_pk>/comments/add/",
                self.comment_create_view.as_view(),
                name="comment-create",
            ),
        ]
        return super().get_urls() + self.post_process_urls(urls)
