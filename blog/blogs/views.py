from django.db.models import Q
from django.views.generic import DetailView, ListView

from blog.blogs.form import PostSearchForm
from blog.blogs.models import Category, Post


class PostListView(ListView):
    model = Post
    template_name = "pages/post-list.html"
    context_object_name = "posts"
    paginate_by = 3
    form_class = PostSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["form"] = self.form_class(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset
        query = self.form.cleaned_data["q"]
        category = self.form.cleaned_data["category"]
        if category:
            queryset = queryset.filter(category=category)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).distinct()

        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = "pages/post-detail.html"
    context_object_name = "post"
