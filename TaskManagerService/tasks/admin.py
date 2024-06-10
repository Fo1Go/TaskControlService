from django.contrib.admin import register, ModelAdmin
from .models import Task, User


@register(User)
class UserAdmin(ModelAdmin):
    ...


@register(Task)
class TaskAdmin(ModelAdmin):
    ...

