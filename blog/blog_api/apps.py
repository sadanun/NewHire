from django.apps import AppConfig
from django.urls import include

from . import urls as blog_api_urls


class BlogApiConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog.blog_api"
    label = "blog_api"

    @property
    def urls(self):
        return include(blog_api_urls)
