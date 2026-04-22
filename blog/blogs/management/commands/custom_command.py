from blogs.models import Category
from blogs.models import Post
from blogs.models import Tag
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with sample blog posts, categories, and tags."

    def handle(self, *_args, **_options):  # pyright: ignore[reportUnusedParameter]
        self.stdout.write("Seeding data...")

        author, created = User.objects.get_or_create(
            email="author@demo.com",
            defaults={"name": "Demo Author"},
        )
        if created:
            author.set_password("password123")
            author.save()

        categories = ["Technology", "Lifestyle", "Coding", "Travel"]
        cat_objects = [
            Category.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name)},
            )[0]
            for name in categories
        ]

        tags = ["Python", "Django", "Web Dev", "Tips", "Vlog"]
        tag_objects = [
            Tag.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name)},
            )[0]
            for name in tags
        ]

        posts_data = [
            {
                "title": "How to build a Django Blog",
                "cat": cat_objects[2],
                "tags": [tag_objects[0], tag_objects[1], tag_objects[2]],
            },
            {
                "title": "Top 10 Travel Destinations 2026",
                "cat": cat_objects[3],
                "tags": [tag_objects[4]],
            },
            {
                "title": "Why Python is still awesome",
                "cat": cat_objects[0],
                "tags": [tag_objects[0], tag_objects[3]],
            },
        ]

        for item in posts_data:
            post, created = Post.objects.get_or_create(
                title=item["title"],
                defaults={
                    "slug": slugify(item["title"]),
                    "body": "This is a sample body content for the post. " * 5,
                    "status": "published",
                    "category": item["cat"],
                    "author": author,
                },
            )

            if created:
                post.tags.set(item["tags"])

        self.stdout.write(self.style.SUCCESS("Successfully seeded blog data!"))
