from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from tasks.models import Epic, Sprint, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "status",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    actions = ["mark_archived"]

    def mark_archived(self, request, queryset):
        queryset.update(status="ARCHIVED")

    def has_change_permission(self, request, obj=None):
        if request.user.has_perm("tasks.change_task"):
            return True
        return False

    def has_add_permission(self, request):
        if request.user.has_perm("tasks.add_task"):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm("tasks.delete_task"):
            return True
        return False

    mark_archived.short_description = "Mark selected tasks as archived"


class SprintAdmin(admin.ModelAdmin):
    ...


class EpicAdmin(admin.ModelAdmin):
    ...


admin.site.register(Task, TaskAdmin)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(Epic, EpicAdmin)

# Create groups for task creator, editor, and admin
creator_group, created = Group.objects.get_or_create(name="Creator")
editor_group, created = Group.objects.get_or_create(name="Editor")
admin_group, created = Group.objects.get_or_create(name="Admin")

# Assign permissions to each group
creator_group.permissions.add(
    Permission.objects.get(codename='add_task')
)
editor_group.permissions.add(
    Permission.objects.get(codename='add_task'),
    Permission.objects.get(codename='change_task'),
)
admin_group.permissions.add(
    Permission.objects.get(codename='add_task'),
    Permission.objects.get(codename='change_task'),
    Permission.objects.get(codename='delete_task'),
)