from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.hashers import make_password


def create_users(sender, **kwargs):
    from django.contrib.auth.models import User

    if User.objects.exists():
        return

    users = [
        {
            "username": "admin",
            "password": "admin",
            "is_superuser": True,
            "is_staff": True,
        },
        {
            "username": "user1",
            "password": "password",
        },
        {
            "username": "user2",
            "password": "password",
        },
    ]

    for user in users:
        User.objects.create(
            username=user["username"],
            password=make_password(user["password"]),
            is_superuser=user.get("is_superuser", False),
            is_staff=user.get("is_staff", False),
        )


class TaskManagerAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_manager_app"

    def ready(self):
        post_migrate.connect(create_users, sender=self)
