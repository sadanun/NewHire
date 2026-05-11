from django.test import TestCase
from django.urls import reverse

from blog.factory.blogs import CategoryFactory, PostFactory, UserFactory


class TestPostListView(TestCase):  # test list view pagination
    PAGE_SIZE = 10

    def setUp(self):
        self.user = UserFactory()
        self.post_1 = PostFactory(author=self.user)
        self.post_2 = PostFactory()
        self.url = reverse("blogs:post-list")
        self.posts = [PostFactory(author=self.user) for _ in range(25)]

    def test_get_post_list(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert self.post_1.title in response.content.decode()
        assert self.post_2.title in response.content.decode()

    def test_post_list_pagination(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert len(response.context["posts"]) == self.PAGE_SIZE
        assert response.context["page_obj"].number == 1

    def test_first_page_returns_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_second_page_returns_200(self):
        response = self.client.get(self.url + "?page=2")
        assert response.status_code == 200
        assert len(response.context["posts"]) == self.PAGE_SIZE
        assert response.context["page_obj"].number == 2


class TestPostDetailView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.posts = PostFactory()
        self.url = reverse("blogs:post-detail", kwargs={"slug": self.posts.slug})

    def test_post_detail_view(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert self.posts.title in response.content.decode()

    def test_nonexistent_post_returns_404(self):  # feature img not found
        url = reverse("blogs:post-detail", kwargs={"slug": "does-not-exist"})
        response = self.client.get(url)
        assert response.status_code == 404


class TestCategorySearch(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory(author=self.user)
        self.post = PostFactory(author=self.user, category=self.category)
        self.url = reverse("blogs:post-list")

    def test_category_search(self):  # search by category in list view
        response = self.client.get(self.url + f"?category={self.category.id}")
        assert response.status_code == 200
        assert self.post.title in response.content.decode()

    def test_title_search(self):  # search by title in list view
        url = reverse("blogs:post-list") + "?q=Sample"
        response = self.client.get(url)
        assert response.status_code == 200
        assert self.post.title in response.content.decode()
