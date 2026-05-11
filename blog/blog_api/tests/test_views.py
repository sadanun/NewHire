from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from blog.blogs.models import Category, Comment, Post
from blog.factory.blogs import CategoryFactory, CommentFactory, PostFactory, UserFactory


class TestPostListAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("blogs_api:post-list")

    def test_post_list_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_list_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert self.post.title in response.content.decode()

    def test_post_create_api(self):
        category = CategoryFactory()
        data = {
            "title": "New Post",
            "body": "This is a new post.",
            "status": "published",
            "category": category.id,
            "author": self.user.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        new_post = Post.objects.filter(title="New Post").first()
        assert new_post is not None


class TestPostDetailAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("blogs_api:post-detail", kwargs={"pk": self.post.id})

    def test_post_detail_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_detail_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert self.post.title in response.content.decode()

    def test_update_post_non_existent(self):
        url = reverse("blogs_api:post-detail", kwargs={"pk": 999})
        category = CategoryFactory()
        data = {
            "title": "Updated Post",
            "body": "This is an updated post.",
            "status": "draft",
            "category": category.id,
            "author": self.user.id,
        }
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_update_api(self):
        category = CategoryFactory()
        data = {
            "title": "Updated Post",
            "body": "This is an updated post.",
            "status": "draft",
            "category": category.id,
            "author": self.user.id,
        }
        response = self.client.put(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        new_post = Post.objects.filter(title="Updated Post").first()
        assert new_post is not None


class TestCategoryListAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("blogs_api:category-list")

    def test_category_list_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_category_list_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert self.category.name in response.content.decode()

    def test_category_create_api(self):
        data = {"name": "Create Category", "slug": "create-category"}
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        new_category = Category.objects.filter(name="Create Category").first()
        assert new_category is not None


class TestCategoryDetailAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("blogs_api:category-detail", kwargs={"pk": self.category.id})

    def test_category_detail_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_category_detail_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert self.category.name in response.content.decode()

    def test_update_category_non_existent(self):
        url = reverse("blogs_api:category-detail", kwargs={"pk": 999})
        data = {"name": "Updated Category", "slug": "updated-category"}
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_category_update_api(self):
        data = {"name": "Updated Category", "slug": "updated-category"}
        response = self.client.put(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        new_category = Category.objects.filter(name="Updated Category").first()
        assert new_category is not None


class TestCommentListAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.comment = CommentFactory(post=self.post, author=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("blogs_api:comment-list")

    def test_comment_list_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_comment_list_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert self.comment.body in response.content.decode()

    def test_comment_create_api(self):
        data = {
            "body": "This is a new comment.",
            "post": self.post.id,
            "author": self.user.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        new_comment = Comment.objects.filter(body="This is a new comment.").first()
        assert new_comment is not None


class TestCommentDetailAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.comment = CommentFactory(post=self.post, author=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("blogs_api:comment-detail", kwargs={"pk": self.comment.id})

    def test_comment_detail_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_comment_detail_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert self.comment.body in response.content.decode()

    def test_update_comment_non_existent(self):
        url = reverse("blogs_api:comment-detail", kwargs={"pk": 999})
        data = {
            "body": "This is an updated comment.",
            "post": self.post.id,
            "author": self.user.id,
        }
        response = self.client.put(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_comment_update_api(self):
        data = {
            "body": "This is an updated comment.",
            "post": self.post.id,
            "author": self.user.id,
        }
        response = self.client.put(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        new_comment = Comment.objects.filter(body="This is an updated comment.").first()
        assert new_comment is not None


class TestCommentListInPostAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.comment = CommentFactory(post=self.post, author=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse(
            "blogs_api:comment-list-in-post", kwargs={"post_id": self.post.id}
        )

    def test_comment_list_in_post_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_comment_list_in_post_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert self.comment.body in response.content.decode()


class TestAllBlogBelongsToCategoryAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.post = PostFactory(author=self.user, category=self.category)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse(
            "blogs_api:all-blog-belongs-to-category",
            kwargs={"category_id": self.category.id},
        )

    def test_all_blog_belongs_to_category_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_all_blog_belongs_to_category_api(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert self.post.title in response.content.decode()
