from django.contrib import admin

from .models import Label, Status, Task, TaskLabel

admin.site.register(Status)
admin.site.register(Task)
admin.site.register(Label)
admin.site.register(TaskLabel)
