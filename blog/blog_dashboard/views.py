from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableMixin

from blog.blog_dashboard.form import (
    CategoryForm,
    CategoryUpdateForm,
    CommentForm,
    PostCreateForm,
    PostUpdateForm,
)
from blog.blog_dashboard.tables import CategoryTable, PostTable
from blog.blogs.models import Category, Comment, Post


class PostListView(SingleTableMixin, ListView):
    model = Post
    table_class = PostTable
    template_name = "post-list.html"
    context_table_name = "posts"


post_list_view = PostListView.as_view()


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "post-create.html"
    context_table_name = "posts"

    def get_success_url(self):
        return reverse("blog_dashboard:post-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


post_create_view = PostCreateView.as_view()


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "post-detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author")
        return ctx


post_detail_view = PostDetailView.as_view()


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = "post-update.html"
    success_url = reverse_lazy("blog_dashboard:post-list")


post_update_view = PostUpdateView.as_view()


class PostDeleteView(DeleteView):
    model = Post
    template_name = "post-delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog_dashboard:post-list")


post_delete_view = PostDeleteView.as_view()


class CategoryListView(SingleTableMixin, ListView):
    model = Category
    table_class = CategoryTable
    template_name = "category-list.html"
    context_table_name = "categories"


category_list_view = CategoryListView.as_view()


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category-create.html"
    success_url = reverse_lazy("blog_dashboard:category-list")

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


category_create_view = CategoryCreateView.as_view()


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryUpdateForm
    template_name = "category-update.html"
    success_url = reverse_lazy("blog_dashboard:category-list")


category_update_view = CategoryUpdateView.as_view()


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category-delete.html"
    context_object_name = "category"
    success_url = reverse_lazy("blog_dashboard:category-list")


category_delete_view = CategoryDeleteView.as_view()


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment-create.html"

    def get_success_url(self):
        post_obj = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        return reverse("blog_dashboard:post-detail", kwargs={"pk": post_obj.pk})

    def form_valid(self, form):
        post_obj = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        form.instance.author_id = self.request.user.id
        form.instance.post_id = post_obj.pk
        return super().form_valid(form)


comment_create_view = CommentCreateView.as_view()


class CommentDeleteView(DeleteView):
    model = Comment
    pk_url_kwarg = "comment_pk"
    http_method_names = ["post"]

    def get_success_url(self):
        comment = self.get_object()
        return reverse("blog_dashboard:post-detail", kwargs={"pk": comment.post_id})


comment_delete_view = CommentDeleteView.as_view()
