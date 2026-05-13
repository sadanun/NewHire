from django.apps import AppConfig
from django.urls import include


class BlogApiConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog.blog_api"
    label = "blog_api"

    @property
    def urls(self):

        from . import urls as blog_api_urls  # noqa: PLC0415

        return include(blog_api_urls)
