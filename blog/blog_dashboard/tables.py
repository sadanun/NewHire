import django_tables2 as tables
from django_tables2.utils import A

from blog.blogs.models import Category, Post


class CategoryTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="tables/category_actions.html",
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = Category
        fields = ("name", "slug", "actions")


class PostTable(tables.Table):
    title = tables.LinkColumn("blog_dashboard:post-detail", args=[A("pk")])
    featured_image = tables.TemplateColumn(
        template_name="tables/post_featured_image.html",
        verbose_name="Featured Image",
        orderable=False,
    )
    actions = tables.TemplateColumn(
        template_name="tables/post_actions.html",
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "slug",
            "category",
            "featured_image",
            "status",
            "author",
            "tags",
            "created_at",
            "actions",
        )
