from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import (
    LabelForm,
    StatusForm,
    TaskForm,
    UserCreateForm,
    UserUpdateForm,
)
from .models import Label, Status, Task

# ================= INDEX =================


def index(request):
    return render(request, "task_manager/index.html")


def test_rollbar_error(request):
    a = None
    a.hello()
    return HttpResponse("Hello, world. You're at the test index.")


# ================= USERS =================


class UsersListView(ListView):
    model = User
    template_name = "task_manager/users/users.html"
    context_object_name = "users"


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "task_manager/users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Пользователь успешно зарегистрирован",
        )
        return response


class UserUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = User
    form_class = UserUpdateForm
    template_name = "task_manager/users/update.html"
    success_url = reverse_lazy("users_list")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно изменен")
        return response

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect("users_list")


class UserDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = User
    template_name = "task_manager/users/delete.html"
    success_url = reverse_lazy("users_list")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect("users_list")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Пользователь успешно удален")
            return response
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется",
            )
            return redirect("users_list")


# ================= STATUSES =================


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "task_manager/statuses/statuses.html"
    context_object_name = "statuses"
    login_url = reverse_lazy("login")


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "task_manager/statuses/create.html"
    success_url = reverse_lazy("statuses_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Статус успешно создан")
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "task_manager/statuses/update.html"
    success_url = reverse_lazy("statuses_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Статус успешно изменен")
        return response


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "task_manager/statuses/delete.html"
    success_url = reverse_lazy("statuses_list")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Статус успешно удален")
            return response
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется",
            )
            return redirect("statuses_list")


# ================= TASKS =================


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "task_manager/tasks/tasks.html"
    context_object_name = "tasks"
    login_url = reverse_lazy("login")
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.select_related(
            "author",
            "executor",
            "status",
        )


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/tasks/create.html"
    success_url = reverse_lazy("tasks_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Задача успешно создана")
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/tasks/update.html"
    success_url = reverse_lazy("tasks_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Задача успешно изменена")
        return response


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_manager/tasks/detail.html"
    context_object_name = "task"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Task.objects.select_related(
            "author",
            "executor",
            "status",
        )


class TaskDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Task
    template_name = "task_manager/tasks/delete.html"
    success_url = reverse_lazy("tasks_list")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object().author

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Задача успешно удалена")
        return response

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks_list")


# ================= LABELS =================


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "task_manager/labels/labels.html"
    context_object_name = "labels"
    login_url = reverse_lazy("login")


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "task_manager/labels/create.html"
    success_url = reverse_lazy("labels_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно создана")
        return response


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "task_manager/labels/update.html"
    success_url = reverse_lazy("labels_list")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Метка успешно изменена")
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "task_manager/labels/delete.html"
    success_url = reverse_lazy("labels_list")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Метка успешно удалена")
            return response
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется",
            )
            return redirect("labels_list")


# ================= AUTH =================


class LoginView(DjangoLoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return response


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
