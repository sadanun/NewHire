from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.blogs.models import Category, Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "featured_image", "category", "tags", "status", "body"]
        widgets = {
            "title": forms.TextInput(),
            "status": forms.Select(),
            "category": forms.Select(),
            "tags": forms.SelectMultiple(),
            "body": CKEditor5Widget(),
            "featured_image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/jpeg,image/png,image/gif,image/webp",
                }
            ),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "featured_image", "category", "tags", "status", "body"]
        widgets = {
            "title": forms.TextInput(),
            "status": forms.Select(),
            "category": forms.Select(),
            "tags": forms.SelectMultiple(),
            "body": CKEditor5Widget(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(),
            "slug": forms.TextInput(),
        }
        labels = {"name": "Category Name", "slug": "Slug"}


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(),
            "slug": forms.TextInput(),
        }
        labels = {"name": "Category Name", "slug": "Slug"}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "write a comment...",
                }
            ),
        }
        labels = {"body": "Comment"}
