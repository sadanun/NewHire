from django.apps import AppConfig


class BlogApiConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog.blog_api"
    label = "blog_api"
