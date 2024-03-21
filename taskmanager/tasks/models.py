from datetime import date
from django.conf import settings
from django.contrib.auth.models import User 
from django.db import models

# Create your models here.
class VersionMixing:
    version = models.IntegerField(default = 0)

class Epic(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    creator = models.ForeignKey(
        User,
        related_name = "created_epic",
        on_delete = models.CASCADE,
    )
    tasks = models.ManyToManyField(
        "Task",
        related_name = "epics",
        blank = True,
    )
    completion_status = models.FloatField(default=0.0)

class Task(VersionMixing, models.Model):
    STATUS_CHOICES = [
        ("UNASSIGNED", "Unassigned"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Completed"),
        ("ARCHIEVED", "Archieved"), 
    ]
    title = models.CharField(max_length = 50)
    description = models.TextField(
        blank = True,
        null = False,
        default = "",
    )
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = "UNASSIGNED",
        db_comment = "can be UNASSIGNED, IN_PROGRESS, DONE or ARCHIEVED.",
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    due_date = models.DateField(default = date.today)

    file_upload = models.FileField(
        upload_to = "tasks/files/",
        null = True,
        blank = True,
    )

    image_upload = models.ImageField(
        upload_to = "tasks/images/",
        null = True,
        blank = True,
    )

    creator = models.ForeignKey(
        User,
        related_name = "created_tasks",
        on_delete = models.CASCADE,
    )

    owner = models.ForeignKey(
        User,
        db_comment = "Forign Key to the User who currently owns the task.",
        related_name = "owend_tasks",
        on_delete = models.SET_NULL,
            null = True,
    )

    class Meta:
        db_table_comment = "Holds Information about tasks"
        constraints = [
            models.CheckConstraint(
                check=models.Q(status="UNASSIGNED")
                | models.Q(status="IN_PROGRESS")
                | models.Q(status="DONE")
                | models.Q(status="ARCHIVED"),
                name="status_check",
            )
        ]

        permissions = [
            (
                "custom_task",
                "Custom Task Permission",
            ),
        ]

class Sprint(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    creator = models.ForeignKey(
        User,
        related_name = "created_sprints",
        on_delete = models.CASCADE,
    )

    tasks = models.ManyToManyField(
        "Task",
        related_name = "sprints",
        blank = True,
    )

    epic = models.ForeignKey(
        Epic, related_name="sprints",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = models.Q(end_date__gt = models.F("start_date")),
                name = "end date_after_start_date",
            ),
        ]

class SubscribedEmail(models.Model):
    email = models.EmailField()
    task = models.ForeignKey(
        Task,
        on_delete = models.CASCADE,
        related_name = "watchers",
    )

class FormSubmission(models.Model):
    uuid = models.UUIDField(unique = True)