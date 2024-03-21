from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from tasks.models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "status", "owner", "created_at", "updated_at") #"due_date"
    list_filter = ("status",)
    actions = ["mark_archived"]

    def mark_archived(self, request, queryset):
        queryset.update(status = "ARCHIVED")
    mark_archived.short_description = "Mark seleected tasks as archived"

    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        if request.user.has_perm("tasks.change_tasks"):
            return True
        return False    

    def has_add_permission(self, request: HttpRequest) -> bool:
        if request.user.has_perm("tasks.add_task"):
            return True
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        if request.user.has_perm("tasks.delete_task"):
            return True
        return False

admin.site.register(Task, TaskAdmin)