from django.contrib import admin
from .models import Status, Task, Label, TaskLabel

admin.site.register(Status)
admin.site.register(Task)
admin.site.register(Label)
admin.site.register(TaskLabel)
