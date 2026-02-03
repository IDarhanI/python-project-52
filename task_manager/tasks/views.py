from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.tasks.models import Task

from .filters import TaskFilter
from .forms import TaskForm


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


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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
