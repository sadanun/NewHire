from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.blogs.models import Category, Comment, Post

from .serializers import CategorySerializer, CommentSerializer, PostSerializer


class PostListViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ["get", "post", "put"]

    @action(detail=True, methods=["get"], url_path="comments")
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CategoryListViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "post", "put"]

    @action(detail=True, methods=["get"], url_path="posts")
    def posts(self, request, pk=None):
        category = self.get_object()
        posts = Post.objects.filter(category=category)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CommentListViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ["get", "post", "put"]
    serializer_class = CommentSerializer
