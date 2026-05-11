from django.test import TestCase
from django.urls import reverse

from blog.blogs.models import Category, Post
from blog.factory.blogs import CategoryFactory, PostFactory, UserFactory


class TestPostListView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post_1 = PostFactory(author=self.user)
        self.post_2 = PostFactory()
        self.url = reverse("blog_dashboard:post-list")

    def test_get_posts(self):
        self.client.login(email=self.user.email, password="password123")
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert self.post_1.title in response.content.decode()
        assert self.post_2.title in response.content.decode()


class TestPostDetailView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.url = reverse("blog_dashboard:post-detail", kwargs={"pk": self.post.pk})

    def test_get_post_detail(self):
        self.client.login(email=self.user.email, password="password123")
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert self.post.title in response.content.decode()


class TestPostCreateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("blog_dashboard:post-create")

    def test_create_post(self):
        self.client.login(email=self.user.email, password="password123")
        category = CategoryFactory()
        data = {
            "title": "New Post",
            "body": "This is a new post.",
            "status": "published",
            "category": category.id,
        }
        response = self.client.post(self.url, data, follow=False)
        assert response.status_code == 302  # Redirect after successful creation
        new_post = Post.objects.filter(title="New Post").first()
        assert new_post is not None
        assert new_post.body == "This is a new post."

    def test_non_authenticated_user_cannot_create_post(self):
        category = CategoryFactory()
        data = {
            "title": "New Post",
            "body": "This is a new post.",
            "status": "published",
            "category": category.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 302  # Redirect to login page
        assert not Post.objects.filter(title="New Post").exists()


class TestPostUpdateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()
        self.post = PostFactory(author=self.user)
        self.url = reverse("blog_dashboard:post-update", kwargs={"pk": self.post.pk})

    def test_update_post_by_non_owner(self):
        self.client.login(email=self.user1.email, password="password123")
        category = CategoryFactory()
        data = {
            "title": "Updated Post",
            "body": "This is an updated post.",
            "status": "published",
            "category": category.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 403

    def test_owner_can_access_update_form(self):
        self.client.login(email=self.user1.email, password="password123")
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_update_post_by_owner(self):
        self.client.login(email=self.user.email, password="password123")
        category = CategoryFactory()
        data = {
            "title": "Updated Post by Staff",
            "body": "This is an updated post by staff.",
            "status": "published",
            "category": category.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert response.url == reverse("blog_dashboard:post-list")
        assert Post.objects.filter(title="Updated Post by Staff").exists()

    def test_non_authenticated_user_cannot_update_post(self):
        response = self.client.post(self.url)
        assert response.status_code == 302
        assert Post.objects.filter(pk=self.post.pk).exists()

    def test_update_post_by_staff_user(self):
        staff_user = UserFactory(is_staff=True)
        self.client.login(email=staff_user.email, password="password123")
        category = CategoryFactory()
        data = {
            "title": "Updated Post by Staff",
            "body": "This is an updated post by staff.",
            "status": "published",
            "category": category.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert response.url == reverse("blog_dashboard:post-list")
        assert Post.objects.filter(title="Updated Post by Staff").exists()


class TestPostDeleteView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()
        self.post = PostFactory(author=self.user)
        self.url = reverse("blog_dashboard:post-delete", kwargs={"pk": self.post.pk})

    def test_delete_post_by_non_owner(self):
        self.client.login(email=self.user1.email, password="password123")
        response = self.client.post(self.url)
        assert response.status_code == 403
        assert Post.objects.filter(pk=self.post.pk).exists()

    def test_delete_post_by_owner(self):
        self.client.login(email=self.user.email, password="password123")
        response = self.client.post(self.url)
        assert response.status_code == 302
        assert not Post.objects.filter(pk=self.post.pk).exists()

    def test_non_authenticated_user_cannot_delete_post(self):
        response = self.client.post(self.url)
        assert response.status_code == 302  # Redirect to login page
        assert Post.objects.filter(pk=self.post.pk).exists()


class TestCategoryListView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category_1 = CategoryFactory(author=self.user)
        self.category_2 = CategoryFactory()
        self.url = reverse("blog_dashboard:category-list")

    def test_get_categories(self):
        self.client.login(email=self.user.email, password="password123")
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert self.category_1.name in response.content.decode()
        assert self.category_2.name in response.content.decode()


class TestCategoryCreateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("blog_dashboard:category-create")

    def test_create_category(self):
        self.client.login(email=self.user.email, password="password123")
        data = {"name": "New Category", "slug": "new-category"}
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert response.url == reverse("blog_dashboard:category-list")
        assert Category.objects.filter(name="New Category").exists()

    def test_non_authenticated_user_cannot_create_category(self):
        data = {"name": "New Category", "slug": "new-category"}
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert not Category.objects.filter(name="New Category").exists()


class TestCategoryUpdateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()
        self.category = CategoryFactory(author=self.user)
        self.url = reverse(
            "blog_dashboard:category-update", kwargs={"pk": self.category.pk}
        )

    def test_update_category_by_non_owner(self):
        self.client.login(email=self.user1.email, password="password123")
        data = {"name": "Updated Category", "slug": "updated-category"}
        response = self.client.post(self.url, data)
        assert response.status_code == 403

    def test_update_category_by_owner(self):
        self.client.login(email=self.user.email, password="password123")
        data = {"name": "Updated Category", "slug": "updated-category"}
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert response.url == reverse("blog_dashboard:category-list")
        assert Category.objects.filter(name="Updated Category").exists()

    def test_non_authenticated_user_cannot_update_category(self):
        data = {"name": "Updated Category", "slug": "updated-category"}
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert Category.objects.filter(pk=self.category.pk).exists()


class TestCategoryDeleteView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()
        self.category = CategoryFactory(author=self.user)
        self.url = reverse(
            "blog_dashboard:category-delete", kwargs={"pk": self.category.pk}
        )

    def test_delete_category_by_non_owner(self):
        self.client.login(email=self.user1.email, password="password123")
        response = self.client.post(self.url)
        assert response.status_code == 403
        assert Category.objects.filter(pk=self.category.pk).exists()

    def test_delete_category_by_owner(self):
        self.client.login(email=self.user.email, password="password123")
        response = self.client.post(self.url)
        assert response.status_code == 302
        assert not Category.objects.filter(pk=self.category.pk).exists()

    def test_non_authenticated_user_cannot_delete_category(self):
        response = self.client.post(self.url)
        assert response.status_code == 302
        assert Category.objects.filter(pk=self.category.pk).exists()


class TestCommentCreateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()
        self.post = PostFactory(author=self.user)
        self.url = reverse(
            "blog_dashboard:comment-create", kwargs={"post_pk": self.post.pk}
        )

    def test_create_comment(self):
        self.client.login(email=self.user1.email, password="password123")
        data = {"body": "This is a comment."}
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert self.post.comments.filter(body="This is a comment.").exists()

    def test_non_authenticated_user_cannot_create_comment(self):
        data = {"body": "This is a comment."}
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert not self.post.comments.filter(body="This is a comment.").exists()

    def test_count_comments_after_creation(self):
        self.client.login(email=self.user1.email, password="password123")
        data = {"body": "This is a comment."}
        self.client.post(self.url, data)
        assert self.post.comments.count() == 1


class TestDeleteCommentView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()
        self.post = PostFactory(author=self.user)

    def test_delete_comment_by_non_owner(self):
        comment = self.post.comments.create(
            body="Comment to delete by non-owner", author=self.user
        )
        self.client.login(email=self.user1.email, password="password123")
        delete_url = reverse(
            "blog_dashboard:comment-delete", kwargs={"comment_pk": comment.pk}
        )
        response = self.client.post(delete_url)
        assert response.status_code == 403
        assert self.post.comments.filter(pk=comment.pk).exists()

    def test_delete_comment_by_owner(self):
        comment = self.post.comments.create(
            body="Comment to delete by owner", author=self.user
        )
        self.client.login(email=self.user.email, password="password123")
        delete_url = reverse(
            "blog_dashboard:comment-delete", kwargs={"comment_pk": comment.pk}
        )
        response = self.client.post(delete_url)
        assert response.status_code == 302
        assert not self.post.comments.filter(pk=comment.pk).exists()
