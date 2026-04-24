from django.db.models import Q
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Category
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "pages/list_view.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(body__icontains=query)  # noqa: E501
            ).distinct()
        return queryset

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get("paginate_by")
        if paginate_by:
            try:
                return int(paginate_by)
            except ValueError:
                pass
        return self.paginate_by


class PostDetailView(DetailView):
    model = Post
    template_name = "pages/detail_view.html"
    context_object_name = "post"



