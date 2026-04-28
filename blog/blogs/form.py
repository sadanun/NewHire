from django import forms

from blog.blogs.models import Category


class PostSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search posts..", "class": "form-control"}
        ),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(
            attrs={"class": "form-select", "onchange": "this.form.submit()"}
        ),
    )
