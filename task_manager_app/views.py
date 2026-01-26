from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django_filters.views import FilterView
from django.http import HttpResponse

from .models import Status, Task, Label
from .forms import UserCreateForm, UserUpdateForm, StatusForm, TaskForm, LabelForm
from .filters import TaskFilter


def index(request):
    return render(request, "task_manager_app/index.html")


def test_rollbar_error(request):
    a = None
    a.hello()
    return HttpResponse("Hello, world. You're at the test index.")


# ================= USERS =================


class UsersListView(ListView):
    model = User
    template_name = "task_manager_app/users/users.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "task_manager_app/users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully registered")


class UserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserUpdateForm
    template_name = "task_manager_app/users/update.html"
    success_url = reverse_lazy("users_list")
    success_message = _("User successfully updated")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object()


class UserDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = User
    template_name = "task_manager_app/users/delete.html"
    success_url = reverse_lazy("users_list")
    success_message = _("User successfully deleted")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object()

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Cannot delete user because it is in use"))
            return redirect("users_list")


# ================= STATUSES =================


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "task_manager_app/statuses/statuses.html"
    context_object_name = "statuses"
    login_url = reverse_lazy("login")


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "task_manager_app/statuses/create.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status successfully created")
    login_url = reverse_lazy("login")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "task_manager_app/statuses/update.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status successfully updated")
    login_url = reverse_lazy("login")


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "task_manager_app/statuses/delete.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status successfully deleted")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Cannot delete status because it is in use"))
            return redirect("statuses_list")


# ================= TASKS =================


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "task_manager_app/tasks/tasks.html"
    context_object_name = "tasks"
    login_url = reverse_lazy("login")
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.select_related("author", "executor", "status")


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager_app/tasks/create.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task successfully created")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager_app/tasks/update.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task successfully updated")
    login_url = reverse_lazy("login")


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_manager_app/tasks/detail.html"
    context_object_name = "task"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Task.objects.select_related("author", "executor", "status")


class TaskDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = "task_manager_app/tasks/delete.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task successfully deleted")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        messages.error(self.request, _("Only task author can delete it"))
        return redirect("tasks_list")


# ================= LABELS =================


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "task_manager_app/labels/labels.html"
    context_object_name = "labels"
    login_url = reverse_lazy("login")


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "task_manager_app/labels/create.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Label successfully created")
    login_url = reverse_lazy("login")


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "task_manager_app/labels/update.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Label successfully updated")
    login_url = reverse_lazy("login")


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "task_manager_app/labels/delete.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("Label successfully deleted")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Cannot delete label because it is in use"))
            return redirect("labels_list")


# ================= AUTH =================


class LoginView(View):
    template_name = "registration/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, _("You are logged in"))
            return redirect("index")

        messages.error(request, _("Please enter correct username and password"))
        return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request):
        logout(request)
        messages.info(request, _("You are logged out"))
        return redirect("index")
