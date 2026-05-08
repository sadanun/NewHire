from django.test import TestCase

from blog.blogs.models import Category, Comment, Post, Tag
from blog.factory.blogs import (
    CategoryFactory,
    CommentFactory,
    PostFactory,
    TagFactory,
    UserFactory,
)


class TestPost(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.post_1 = PostFactory(author=self.user)
        self.post_2 = PostFactory(author=self.user2)

    def test_get_posts(self):
        posts = Post.objects.all()
        assert posts.count() == 2
        assert self.post_1 in posts
        assert self.post_2 in posts

    def test_post_auto_slug(self):
        assert self.post_1.slug == self.post_1.title.lower().replace(" ", "-")
        assert self.post_2.slug == self.post_2.title.lower().replace(" ", "-")

    def test_status_default(self):
        assert self.post_1.status == "draft"
        assert self.post_2.status == "draft"


class TestCategory(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category_1 = CategoryFactory(author=self.user)
        self.category_2 = CategoryFactory()

    def test_get_categories(self):
        categories = Category.objects.all()
        assert categories.count() == 2
        assert self.category_1 in categories
        assert self.category_2 in categories

    def test_category_representation(self):
        assert str(self.category_1) == self.category_1.name
        assert str(self.category_2) == self.category_2.name


class TestTag(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.tag_1 = TagFactory(author=self.user)
        self.tag_2 = TagFactory()

    def test_get_tags(self):
        tags = Tag.objects.all()
        assert tags.count() == 2
        assert self.tag_1 in tags
        assert self.tag_2 in tags

    def test_tag_representation(self):
        assert str(self.tag_1) == self.tag_1.name
        assert str(self.tag_2) == self.tag_2.name


class TestComment(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.comment_1 = CommentFactory(post=self.post, author=self.user)
        self.comment_2 = CommentFactory(post=self.post)

    def test_get_comments(self):
        comments = Comment.objects.all()
        assert comments.count() == 2
        assert self.comment_1 in comments
        assert self.comment_2 in comments

    def test_comment_relationships(self):
        assert self.comment_1.post == self.post
        assert self.comment_1.author == self.user
        assert self.comment_2.post == self.post
        assert self.comment_2.author == self.comment_2.author
