import django_tables2 as tables
from django_tables2.utils import A

from blog.blogs.models import Category, Post


class CategoryTable(tables.Table):
    actions = tables.TemplateColumn(
        template_code="""
            <div class="btn-group btn-group-sm" role="group">
                {% if request.user.is_staff %}
                    <a href="{% url 'blog_dashboard:category-update' record.pk %}"
                    class="btn btn-warning" title="Edit">
                        <i class="bi bi-pencil"></i> Edit
                    </a>
                {% endif %}
                {% if user.is_staff or record.author_id == user.id %}
                    <a href="{% url 'blog_dashboard:category-delete' record.pk %}"
                    class="btn btn-danger" title="Delete"
                    onclick="return confirm('Delete this category?');">
                        <i class="bi bi-trash"></i> Delete
                    </a>
                {% endif %}
            </div>
        """,
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = Category
        fields = ("name", "slug", "actions")


class PostTable(tables.Table):
    title = tables.LinkColumn("blog_dashboard:post-detail", args=[A("pk")])
    featured_image = tables.TemplateColumn(
        template_code="""
            {% if record.featured_image %}
                <a href="{{ record.featured_image.url }}">
                    <img src="{{ record.featured_image.url }}"
                         style="width:50px; border-radius:4px;" />
                </a>
            {% else %}
                —
            {% endif %}
        """,
        verbose_name="Featured Image",
        orderable=False,
    )
    actions = tables.TemplateColumn(
        template_code="""
            <div class="float-right">
                {% if record.author_id == user.id or user.is_staff %}
                    <div class="btn-group btn-group-sm" role="group">
                        <a href="{% url 'blog_dashboard:post-update' record.pk %}"
                        class="btn btn-warning" title="Edit">
                            <i class="bi bi-pencil"></i> Edit
                        </a>
                        <a href="{% url 'blog_dashboard:post-delete' record.pk %}"
                        class="btn btn-danger" title="Delete"
                        onclick="return confirm('Delete this post?');">
                            <i class="bi bi-trash"></i> Delete
                        </a>
                    </div>
                {% endif %}
            </div>
        """,
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
