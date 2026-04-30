from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.blogs.models import Category, Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "featured_image", "category", "tags", "status", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "body": CKEditor5Widget(config_name="default"),
            "featured_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png,image/gif,image/webp",
                }
            ),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "featured_image", "category", "tags", "status", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "body": CKEditor5Widget(config_name="default"),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {"name": "Category Name", "slug": "Slug"}


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {"name": "Category Name", "slug": "Slug"}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "write a comment...",
                }
            ),
        }
        labels = {"body": "Comment"}
