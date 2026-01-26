from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_users(apps, schema_editor):
    User = apps.get_model("auth", "User")

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


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager_app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]
