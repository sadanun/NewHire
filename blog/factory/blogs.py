import factory

from blog.blogs.models import Category, Comment, Post, Tag
from blog.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = "John Doe"
    email = factory.Sequence(lambda n: f"example{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    is_staff = False
    is_active = True


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory("blog.factory.blogs.UserFactory")
    title = factory.Sequence(lambda n: f"Sample Post {n}")
    body = "This is a sample post."
    category = factory.SubFactory("blog.factory.blogs.CategoryFactory")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")
    author = factory.SubFactory("blog.factory.blogs.UserFactory")


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory("blog.factory.blogs.PostFactory")
    author = factory.SubFactory("blog.factory.blogs.UserFactory")
    body = "This is a sample comment."


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"Tag {n}")
    slug = factory.Sequence(lambda n: f"tag-{n}")
    author = factory.SubFactory("blog.factory.blogs.UserFactory")
