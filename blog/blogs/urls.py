from django.urls import path

from .views import post_detail_view, post_list_view

app_name = "blogs"
urlpatterns = [
    path("", view=post_list_view, name="post-list"),
    path("<slug:slug>/", view=post_detail_view, name="post-detail"),
]
