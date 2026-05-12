from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog.blog_api import views

router = DefaultRouter()
router.register(r"posts", views.PostListViewSet, basename="posts")
router.register(r"categories", views.CategoryListViewSet, basename="categories")
router.register(r"comments", views.CommentListViewSet, basename="comments")
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    views.CommentListInPostViewSet,
    basename="post-comments",
)
router.register(
    r"categories/(?P<category_id>\d+)/posts",
    views.AllBlogBelongsToCategoryViewSet,
    basename="category-posts",
)


app_name = "blog_api"
urlpatterns = [
    path("", include(router.urls)),
]
