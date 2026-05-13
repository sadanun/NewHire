from django.test import TestCase

from blog.blog_api.serializers import (
    CategorySerializer,
    CommentSerializer,
    PostSerializer,
)
from blog.factory.blogs import CategoryFactory, CommentFactory, PostFactory, UserFactory


class TestPostSerializer(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.post = PostFactory(author=self.user, category=self.category)
        self.serializer = PostSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        expected_keys = set(
            {
                "id",
                "title",
                "slug",
                "body",
                "featured_image",
                "status",
                "created_at",
                "updated_at",
                "category",
                "author",
                "tags",
            }
        )
        data = self.serializer.data
        assert set(data.keys()) == expected_keys

    def test_missing_title_returns_error(self):
        payload = {
            "body": "...",
            "author": self.user.id,
            "category": self.category.id,
        }
        serializer = PostSerializer(data=payload)
        assert not serializer.is_valid()
        assert "title" in serializer.errors


class TestCategorySerializer(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        expected_keys = set({"id", "name", "slug", "author"})
        data = self.serializer.data
        assert set(data.keys()) == expected_keys

    def test_missing_name_returns_error(self):
        payload = {}
        serializer = CategorySerializer(data=payload)
        assert not serializer.is_valid()
        assert "name" in serializer.errors


class TestCommentSerializer(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.post = PostFactory(author=self.user, category=self.category)
        self.comment = CommentFactory(post=self.post, author=self.user)
        self.serializer = CommentSerializer(instance=self.comment)

    def test_contains_expected_fields(self):
        expected_keys = set({"id", "post", "author", "body", "created_at"})
        data = self.serializer.data
        assert set(data.keys()) == expected_keys

    def test_missing_body_returns_error(self):
        payload = {
            "post": self.post.id,
            "author": self.user.id,
        }
        serializer = CommentSerializer(data=payload)
        assert not serializer.is_valid()
        assert "body" in serializer.errors
