from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Label, Status, Task

User = get_user_model()


# ================= USERS =================


class UserCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )

    def test_user_registration(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "username": "janesmith",
                "password1": "strongpass123",
                "password2": "strongpass123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="janesmith").exists())

    def test_user_update(self):
        self.client.login(
            username="testuser",
            password="testpass123",
        )

        response = self.client.post(
            reverse("user_update", kwargs={"pk": self.user.id}),
            {
                "first_name": "Updated",
                "last_name": "User",
                "username": "updateduser",
            },
        )
        self.assertRedirects(response, reverse("users_list"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_user_delete(self):
        self.client.login(
            username="testuser",
            password="testpass123",
        )

        response = self.client.post(
            reverse("user_delete", kwargs={"pk": self.user.id}),
        )
        self.assertRedirects(response, reverse("users_list"))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_users_list_accessible_without_auth(self):
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Users"))


# ================= STATUSES =================


class StatusCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user",
            password="pass123",
        )
        cls.status = Status.objects.create(name="In Progress")

    def test_status_create(self):
        self.client.login(
            username="user",
            password="pass123",
        )

        response = self.client.post(
            reverse("status_create"),
            {"name": "New"},
        )
        self.assertRedirects(response, reverse("statuses_list"))
        self.assertTrue(Status.objects.filter(name="New").exists())

    def test_status_update(self):
        self.client.login(
            username="user",
            password="pass123",
        )

        response = self.client.post(
            reverse("status_update", kwargs={"pk": self.status.id}),
            {"name": "Updated"},
        )
        self.assertRedirects(response, reverse("statuses_list"))

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated")

    def test_status_delete(self):
        self.client.login(
            username="user",
            password="pass123",
        )

        response = self.client.post(
            reverse("status_delete", kwargs={"pk": self.status.id}),
        )
        self.assertRedirects(response, reverse("statuses_list"))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_statuses_require_login(self):
        response = self.client.get(reverse("statuses_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)


# ================= TASKS =================


class TaskCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="author",
            password="pass",
        )
        cls.executor = User.objects.create_user(
            username="executor",
            password="pass",
        )
        cls.status = Status.objects.create(name="New")

        cls.task = Task.objects.create(
            name="Test task",
            description="Desc",
            status=cls.status,
            author=cls.user,
            executor=cls.executor,
        )

    def test_task_create(self):
        self.client.login(
            username="author",
            password="pass",
        )

        response = self.client.post(
            reverse("task_create"),
            {
                "name": "Created task",
                "description": "Text",
                "status": self.status.id,
                "executor": self.executor.id,
            },
        )
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertTrue(Task.objects.filter(name="Created task").exists())

    def test_task_update(self):
        self.client.login(
            username="author",
            password="pass",
        )

        response = self.client.post(
            reverse("task_update", kwargs={"pk": self.task.id}),
            {
                "name": "Updated task",
                "description": "",
                "status": self.status.id,
                "executor": self.executor.id,
            },
        )
        self.assertRedirects(response, reverse("tasks_list"))

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated task")

    def test_task_delete_by_author(self):
        self.client.login(
            username="author",
            password="pass",
        )

        response = self.client.post(
            reverse("task_delete", kwargs={"pk": self.task.id}),
        )
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


# ================= LABELS =================


class LabelCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user",
            password="pass",
        )
        cls.label = Label.objects.create(name="Bug")

    def test_label_create(self):
        self.client.login(
            username="user",
            password="pass",
        )

        response = self.client.post(
            reverse("label_create"),
            {"name": "Feature"},
        )
        self.assertRedirects(response, reverse("labels_list"))
        self.assertTrue(Label.objects.filter(name="Feature").exists())

    def test_label_update(self):
        self.client.login(
            username="user",
            password="pass",
        )

        response = self.client.post(
            reverse("label_update", kwargs={"pk": self.label.id}),
            {"name": "Updated"},
        )
        self.assertRedirects(response, reverse("labels_list"))

        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated")

    def test_label_delete(self):
        self.client.login(
            username="user",
            password="pass",
        )

        response = self.client.post(
            reverse("label_delete", kwargs={"pk": self.label.id}),
        )
        self.assertRedirects(response, reverse("labels_list"))
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())
