from django.test import TestCase

from blog.blogs.form import PostSearchForm
from blog.factory.blogs import CategoryFactory


class TestPostSearchForm(TestCase):
    def setUp(self):
        self.category = CategoryFactory()

    def test_form_valid_data(self):
        form_data = {
            "q": "Test",
            "category": self.category.id,
        }
        form = PostSearchForm(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data["q"] == "Test"
        assert form.cleaned_data["category"] == self.category

    def test_form_empty_data(self):
        form = PostSearchForm(data={})
        assert form.is_valid()
        assert form.cleaned_data["q"] == ""
        assert form.cleaned_data["category"] is None
