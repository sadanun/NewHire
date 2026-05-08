from django import forms
from django.test import TestCase
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.blog_dashboard.form import (
    CategoryForm,
    CategoryUpdateForm,
    CommentForm,
    PostCreateForm,
    PostUpdateForm,
)
from blog.factory.blogs import PostFactory


class TestPostCreateForm(TestCase):
    def test_widgets(self):
        form = PostCreateForm()
        assert form.fields["title"].widget.__class__ == forms.TextInput
        assert (
            form.fields["featured_image"].widget.__class__ == forms.ClearableFileInput
        )
        assert form.fields["category"].widget.__class__ == forms.Select
        assert form.fields["tags"].widget.__class__ == forms.SelectMultiple
        assert form.fields["status"].widget.__class__ == forms.Select
        assert form.fields["body"].widget.__class__ == CKEditor5Widget

    def test_featured_image_accept_attribute(self):
        form = PostCreateForm()
        featured_image_widget = form.fields["featured_image"].widget
        assert (
            featured_image_widget.attrs["accept"]
            == "image/jpeg,image/png,image/gif,image/webp"
        )


class TestPostUpdateForm(TestCase):
    def setUp(self):
        self.post = PostFactory()

    def test_widgets(self):
        form = PostUpdateForm()
        assert form.fields["title"].widget.__class__ == forms.TextInput
        assert (
            form.fields["featured_image"].widget.__class__ == forms.ClearableFileInput
        )
        assert form.fields["category"].widget.__class__ == forms.Select
        assert form.fields["tags"].widget.__class__ == forms.SelectMultiple
        assert form.fields["status"].widget.__class__ == forms.Select
        assert form.fields["body"].widget.__class__ == CKEditor5Widget


class TestCategoryForm(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "name": "Test Category",
            "slug": "test-category",
        }
        form = CategoryForm(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data["name"] == "Test Category"
        assert form.cleaned_data["slug"] == "test-category"


class TestCategoryUpdateForm(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "name": "Updated Test Category",
            "slug": "updated-test-category",
        }
        form = CategoryUpdateForm(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data["name"] == "Updated Test Category"
        assert form.cleaned_data["slug"] == "updated-test-category"


class TestCommentForm(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "body": "This is a test comment.",
        }
        form = CommentForm(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data["body"] == "This is a test comment."
