from django.apps import AppConfig


class BlogConfig(AppConfig):
    label = "blog"
    name = f"applications.{label}"