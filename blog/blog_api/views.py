from rest_framework import viewsets

from blog.blogs.models import Category, Comment, Post

from .serializers import CategorySerializer, CommentSerializer, PostSerializer


class PostListViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ["get", "post", "put"]


class CategoryListViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "post", "put"]


class CommentListViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ["get", "post", "put"]
    serializer_class = CommentSerializer


class CommentListInPostViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)


class AllBlogBelongsToCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Post.objects.filter(category_id=category_id)
