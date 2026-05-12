from rest_framework import mixins, viewsets

from blog.blogs.models import Category, Comment, Post

from .serializers import CategorySerializer, CommentSerializer, PostSerializer


class PostListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListInPostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)


class AllBlogBelongsToCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Post.objects.filter(category_id=category_id)
