from django.contrib import admin

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task, TaskLabel

admin.site.register(Status)
admin.site.register(Task)
admin.site.register(Label)
admin.site.register(TaskLabel)
