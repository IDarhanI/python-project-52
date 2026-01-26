from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Status, Task, Label

User = get_user_model()


class UserCRUDTest(TestCase):
    def setUp(self):
        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    # Тест создания пользователя (C)
    def test_user_registration(self):
        response = self.client.post(reverse("user_create"), self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username="johndoe").exists())

    # Тест обновления пользователя (U)
    def test_user_update(self):
        self.client.login(username="testuser", password="testpass123")

        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "username": "updateduser",
        }

        response = self.client.post(
            reverse("user_update", kwargs={"pk": self.user.id}), update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))

        # Проверяем обновление данных
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.username, "updateduser")

    # Тест удаления пользователя (D)
    def test_user_delete(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(reverse("user_delete", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))

        # Проверяем, что пользователь удален
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    # Тест, что нельзя удалить другого пользователя
    def test_cannot_delete_other_user(self):
        other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )

        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("user_delete", kwargs={"pk": other_user.id})
        )
        self.assertIn(response.status_code, [403, 404])  # Forbidden

    # Тест списка пользователей доступен без авторизации
    def test_users_list_accessible_without_auth(self):
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Users")


class StatusCRUDTest(TestCase):  # Новый класс для тестов статусов
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.status_data = {"name": "New"}
        self.status = Status.objects.create(name="In Progress")

    # Тест создания статуса (C)
    def test_status_create(self):
        # 1. Авторизуемся
        login_success = self.client.login(username="testuser", password="testpass123")
        self.assertTrue(login_success, "Login should succeed")

        # 2. Получаем правильный URL (с префиксом языка)
        # Принудительно устанавливаем язык для теста
        from django.utils.translation import activate

        activate("en")

        url = reverse("status_create")
        print(f"DEBUG: URL with language prefix: {url}")

        # 3. Проверяем GET запрос
        get_response = self.client.get(url)
        print(f"DEBUG: GET status: {get_response.status_code}")

        # Если все еще редирект, проверяем куда
        if get_response.status_code == 302:
            print(f"DEBUG: Redirect to: {get_response.url}")
            # Следуем за редиректом
            get_response = self.client.get(url, follow=True)
            print(f"DEBUG: After follow: {get_response.status_code}")

        self.assertEqual(
            get_response.status_code,
            200,
            f"Expected 200, got {get_response.status_code}. "
            f"Content: {get_response.content[:500]}",
        )

        # 4. Проверяем наличие формы
        self.assertContains(get_response, 'name="name"')
        self.assertContains(get_response, "csrfmiddlewaretoken")

        # 5. Проверяем POST запрос
        # Нужно получить CSRF токен из формы
        import re

        csrf_match = re.search(
            r'name="csrfmiddlewaretoken" value="([^"]+)"', get_response.content.decode()
        )
        if csrf_match:
            csrf_token = csrf_match.group(1)
            post_data = self.status_data.copy()
            post_data["csrfmiddlewaretoken"] = csrf_token

            post_response = self.client.post(url, post_data)
        else:
            # Без CSRF, но в тестах можно отключить проверку
            post_response = self.client.post(url, self.status_data)

        print(f"DEBUG: POST status: {post_response.status_code}")

        # Проверяем результат
        self.assertIn(post_response.status_code, [200, 302])

        # Если редирект, проверяем куда
        if post_response.status_code == 302:
            self.assertRedirects(post_response, reverse("statuses_list"))

        # Проверяем что статус создан
        self.assertTrue(Status.objects.filter(name="New").exists())

    # Тест обновления статуса (U)
    def test_status_update(self):
        self.client.login(username="testuser", password="testpass123")

        update_data = {"name": "Updated Status"}

        response = self.client.post(
            reverse("status_update", kwargs={"pk": self.status.id}), update_data
        )
        self.assertIn(response.status_code, [200, 302])

        if response.status_code == 302:
            self.assertRedirects(response, reverse("statuses_list"))

        # Проверяем обновление данных
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

    # Тест удаления статуса (D)
    def test_status_delete(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("status_delete", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("statuses_list"))

        # Проверяем, что статус удален
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    # Тест, что статусы доступны только авторизованным
    def test_statuses_require_login(self):
        # Без авторизации должен быть редирект на логин
        response = self.client.get(reverse("statuses_list"), follow=False)
        self.assertEqual(response.status_code, 302)

        # Проверяем что редирект ведет на логин
        # С i18n будет /en/login/ или /ru/login/, а не просто /login/
        self.assertIn("/login/", response.url)
        self.assertIn("next=", response.url)

    # Тест списка статусов доступен при авторизации
    def test_statuses_list_accessible_with_auth(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("statuses_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Statuses")


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        self.status = Status.objects.create(name="New")

        self.task_data = {
            "name": "Test Task",
            "description": "Test description",
            "status": self.status.id,
            "executor": self.other_user.id,
        }

        self.task = Task.objects.create(
            name="Existing Task",
            description="Existing description",
            status=self.status,
            author=self.user,
            executor=self.other_user,
        )

    # Тест создания задачи (C)
    def test_task_create(self):
        self.client.login(username="testuser", password="testpass123")

        # Проверяем GET запрос
        get_response = self.client.get(reverse("task_create"))
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, 'name="name"')

        # Проверяем POST запрос
        post_response = self.client.post(reverse("task_create"), self.task_data)
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse("tasks_list"))

        # Проверяем, что задача создана с правильным автором
        task = Task.objects.get(name="Test Task")
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.executor, self.other_user)
        self.assertEqual(task.status, self.status)

    # Тест обновления задачи (U)
    def test_task_update(self):
        self.client.login(username="testuser", password="testpass123")

        update_data = {
            "name": "Updated Task",
            "description": "Updated description",
            "status": self.status.id,
            "executor": self.user.id,  # Меняем исполнителя
        }

        response = self.client.post(
            reverse("task_update", kwargs={"pk": self.task.id}), update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))

        # Проверяем обновление данных
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")
        self.assertEqual(self.task.executor, self.user)

    # Тест просмотра задачи (R - read detail)
    def test_task_detail(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("task_detail", kwargs={"pk": self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)

    # Тест удаления задачи (D) автором
    def test_task_delete_by_author(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(reverse("task_delete", kwargs={"pk": self.task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))

        # Проверяем, что задача удалена
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    # Тест, что нельзя удалить задачу не автором
    def test_cannot_delete_task_not_by_author(self):
        # Создаем задачу от другого пользователя
        other_task = Task.objects.create(
            name="Other Task",
            description="Other description",
            status=self.status,
            author=self.other_user,
            executor=self.user,
        )

        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("task_delete", kwargs={"pk": other_task.id})
        )
        # Должен быть редирект с сообщением об ошибке
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))

        # Проверяем, что задача НЕ удалена
        self.assertTrue(Task.objects.filter(id=other_task.id).exists())

    # Тест, что задачи требуют авторизации
    def test_tasks_require_login(self):
        # Без авторизации должен быть редирект на логин
        response = self.client.get(reverse("tasks_list"), follow=False)
        self.assertEqual(response.status_code, 302)

        # Проверяем что редирект ведет на логин
        self.assertIn("/login/", response.url)
        self.assertIn("next=", response.url)

    # Тест списка задач доступен при авторизации
    def test_tasks_list_accessible_with_auth(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("tasks_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tasks")

    # Тест flash сообщений
    def test_task_create_flash_message(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(reverse("task_create"), self.task_data, follow=True)
        self.assertContains(response, _("Task successfully created"))

    def test_task_update_flash_message(self):
        self.client.login(username="testuser", password="testpass123")

        # Используем полные данные вместо минимальных
        update_data = {
            "name": "Updated",
            "description": "",
            "status": self.status.id,
            "executor": self.other_user.id,  # Укажем исполнителя явно
        }

        response = self.client.post(
            reverse("task_update", kwargs={"pk": self.task.id}),
            update_data,
            follow=True,
        )

        print(f"DEBUG: Response status: {response.status_code}")
        print(f"DEBUG: Response content (first 500 chars): {response.content[:500]}")

        # Проверяем что страница загрузилась
        self.assertEqual(response.status_code, 200)

        # Проверяем сообщение
        self.assertContains(response, _("Task successfully updated"))

    def test_task_delete_flash_message(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("task_delete", kwargs={"pk": self.task.id}), follow=True
        )
        self.assertContains(response, _("Task successfully deleted"))


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.label_data = {"name": "Bug"}
        self.label = Label.objects.create(name="Feature")

    # Тест создания метки (C)
    def test_label_create(self):
        self.client.login(username="testuser", password="testpass123")

        # Проверяем GET запрос
        get_response = self.client.get(reverse("label_create"))
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, 'name="name"')

        # Проверяем POST запрос
        post_response = self.client.post(reverse("label_create"), self.label_data)
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse("labels_list"))

        # Проверяем, что метка создана
        self.assertTrue(Label.objects.filter(name="Bug").exists())

    # Тест обновления метки (U)
    def test_label_update(self):
        self.client.login(username="testuser", password="testpass123")

        update_data = {"name": "Urgent"}

        response = self.client.post(
            reverse("label_update", kwargs={"pk": self.label.id}), update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))

        # Проверяем обновление данных
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Urgent")

    # Тест удаления метки (D)
    def test_label_delete(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("label_delete", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))

        # Проверяем, что метка удалена
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    # Тест, что нельзя удалить метку связанную с задачей
    def test_cannot_delete_label_in_use(self):
        self.client.login(username="testuser", password="testpass123")

        # Создаем задачу с этой меткой
        status = Status.objects.create(name="Test Status")
        task = Task.objects.create(
            name="Test Task",
            description="Test description",
            status=status,
            author=self.user,
        )
        task.labels.add(self.label)

        # Получаем URL с учетом i18n
        from django.utils.translation import activate

        activate("en")

        url = reverse("label_delete", kwargs={"pk": self.label.id})
        print(f"DEBUG: Label delete URL: {url}")

        # Пытаемся удалить метку
        response = self.client.post(url, follow=False)
        print(f"DEBUG: Response status: {response.status_code}")

        # Если 404, проверяем альтернативные URL
        if response.status_code == 404:
            # Попробуем без префикса языка
            simple_url = f"/labels/{self.label.id}/delete/"
            print(f"DEBUG: Trying simple URL: {simple_url}")
            response = self.client.post(simple_url, follow=False)
            print(f"DEBUG: Simple URL response: {response.status_code}")

        # Должен быть редирект (302) на список меток
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))

        # Проверяем, что метка НЕ удалена
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())

    # Тест, что метки требуют авторизации
    def test_labels_require_login(self):
        # Без авторизации должен быть редирект на логин
        response = self.client.get(reverse("labels_list"), follow=False)
        self.assertEqual(response.status_code, 302)

        # Проверяем что редирект ведет на логин
        self.assertIn("/login/", response.url)
        self.assertIn("next=", response.url)

    # Тест списка меток доступен при авторизации
    def test_labels_list_accessible_with_auth(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("labels_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Labels")

    # Тест добавления меток к задаче
    def test_task_with_labels(self):
        self.client.login(username="testuser", password="testpass123")

        # Создаем вторую метку
        label2 = Label.objects.create(name="Documentation")
        status = Status.objects.create(name="New")

        # Создаем задачу с метками (всегда указываем исполнителя)
        task_data = {
            "name": "Task with labels",
            "description": "Test description",
            "status": status.id,
            "executor": self.user.id,  # Всегда указываем исполнителя
            "labels": [self.label.id, label2.id],
        }

        response = self.client.post(reverse("task_create"), task_data, follow=True)

        self.assertEqual(response.status_code, 200)

        # Проверяем, что задача создана с метками
        task = Task.objects.get(name="Task with labels")
        self.assertEqual(task.labels.count(), 2)
        self.assertIn(self.label, task.labels.all())
        self.assertIn(label2, task.labels.all())

    # Тест flash сообщений
    def test_label_create_flash_message(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("label_create"), self.label_data, follow=True
        )
        self.assertContains(response, _("Label successfully created"))

    def test_label_update_flash_message(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("label_update", kwargs={"pk": self.label.id}),
            {"name": "Updated"},
            follow=True,
        )
        self.assertContains(response, _("Label successfully updated"))

    def test_label_delete_flash_message(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("label_delete", kwargs={"pk": self.label.id}), follow=True
        )
        self.assertContains(response, _("Label successfully deleted"))


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")

        self.status1 = Status.objects.create(name="New")
        self.status2 = Status.objects.create(name="In Progress")

        self.label1 = Label.objects.create(name="Bug")
        self.label2 = Label.objects.create(name="Feature")

        # Создаем тестовые задачи
        self.task1 = Task.objects.create(
            name="Task 1 - Bug",
            description="Bug fix",
            status=self.status1,
            author=self.user1,
            executor=self.user2,
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name="Task 2 - Feature",
            description="New feature",
            status=self.status2,
            author=self.user2,
            executor=self.user1,
        )
        self.task2.labels.add(self.label2)

        self.task3 = Task.objects.create(
            name="Task 3 - Another Bug",
            description="Another bug fix",
            status=self.status1,
            author=self.user1,
            executor=None,
        )
        self.task3.labels.add(self.label1, self.label2)

    # Тест фильтрации по статусу
    def test_filter_by_status(self):
        self.client.login(username="user1", password="testpass123")

        # Фильтруем по статусу "New"
        response = self.client.get(reverse("tasks_list"), {"status": self.status1.id})

        self.assertEqual(response.status_code, 200)
        # Должны быть задачи со статусом New
        self.assertContains(response, "Task 1 - Bug")
        self.assertContains(response, "Task 3 - Another Bug")
        # Не должно быть задач со статусом In Progress
        self.assertNotContains(response, "Task 2 - Feature")

    # Тест фильтрации по исполнителю
    def test_filter_by_executor(self):
        self.client.login(username="user1", password="testpass123")

        # Фильтруем по исполнителю user1
        response = self.client.get(reverse("tasks_list"), {"executor": self.user1.id})

        self.assertEqual(response.status_code, 200)
        # Должна быть задача где user1 исполнитель
        self.assertContains(response, "Task 2 - Feature")
        # Не должно быть задач где user1 не исполнитель
        self.assertNotContains(response, "Task 1 - Bug")

    # Тест фильтрации по метке
    def test_filter_by_label(self):
        self.client.login(username="user1", password="testpass123")

        # Фильтруем по метке "Bug" - ИСПРАВЛЕНО: было labels, стало label
        response = self.client.get(
            reverse("tasks_list"),
            {"label": self.label1.id},  # ИСПРАВЛЕНО
        )

        self.assertEqual(response.status_code, 200)
        # Должны быть задачи с меткой Bug
        self.assertContains(response, "Task 1 - Bug")
        self.assertContains(response, "Task 3 - Another Bug")
        # Не должно быть задач без метки Bug
        self.assertNotContains(response, "Task 2 - Feature")

    # Тест фильтрации "только мои задачи"
    def test_filter_self_tasks(self):
        self.client.login(username="user1", password="testpass123")

        # Фильтруем только задачи user1
        response = self.client.get(reverse("tasks_list"), {"self_tasks": "true"})

        self.assertEqual(response.status_code, 200)
        # Должны быть задачи автором которых является user1
        self.assertContains(response, "Task 1 - Bug")
        self.assertContains(response, "Task 3 - Another Bug")
        # Не должно быть задач других авторов
        self.assertNotContains(response, "Task 2 - Feature")

    # Тест комбинированной фильтрации
    def test_combined_filter(self):
        self.client.login(username="user1", password="testpass123")

        # Фильтруем: статус New + метка Bug - ИСПРАВЛЕНО: было labels, стало label
        response = self.client.get(
            reverse("tasks_list"),
            {
                "status": self.status1.id,
                "label": self.label1.id,  # ИСПРАВЛЕНО
            },
        )

        self.assertEqual(response.status_code, 200)
        # Должны быть задачи со статусом New И меткой Bug
        self.assertContains(response, "Task 1 - Bug")
        self.assertContains(
            response, "Task 3 - Another Bug"
        )  # ИСПРАВЛЕНО: должно содержать
        # Не должно быть задач со статусом New но без метки Bug (таких нет в тестовых данных)
        # Не должно быть задач с другим статусом
        self.assertNotContains(response, "Task 2 - Feature")

    # Тест сброса фильтров
    def test_reset_filters(self):
        self.client.login(username="user1", password="testpass123")

        # Сначала фильтруем
        response = self.client.get(reverse("tasks_list"), {"status": self.status1.id})

        self.assertEqual(response.status_code, 200)
        filtered_count = len(response.context["tasks"])

        # Потом сбрасываем (пустой GET запрос)
        response = self.client.get(reverse("tasks_list"))

        self.assertEqual(response.status_code, 200)
        all_count = len(response.context["tasks"])

        # Всех задач должно быть больше чем отфильтрованных
        self.assertGreater(all_count, filtered_count)
        # Все 3 задачи должны быть видны
        self.assertContains(response, "Task 1 - Bug")
        self.assertContains(response, "Task 2 - Feature")
        self.assertContains(response, "Task 3 - Another Bug")
