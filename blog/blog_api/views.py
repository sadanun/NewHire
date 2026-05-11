from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blog.blogs.models import Category, Comment, Post

from .serializers import CategorySerializer, CommentSerializer, PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


posts_list = PostList.as_view()


class PostDetail(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


post_detail = PostDetail.as_view()


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


category_list = CategoryList.as_view()


class CategoryDetail(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


category_detail = CategoryDetail.as_view()


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


comment_list = CommentList.as_view()


class CommentDetail(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


comment_detail = CommentDetail.as_view()


class CommentListInPost(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)


comment_list_in_post = CommentListInPost.as_view()


class AllBlogBelongsToCategory(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Post.objects.filter(category_id=category_id)


all_blog_belongs_to_category = AllBlogBelongsToCategory.as_view()
