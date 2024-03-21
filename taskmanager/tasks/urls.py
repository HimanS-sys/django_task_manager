from django.urls import path, register_converter
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import converters

register_converter(converters.DateConverter, "yyyymmdd")

from .views import (
    ContactFormView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListView,
    create_task_on_sprint,
    manage_epic_tasks,
    task_home,
    task_by_date,
)
app_name = "tasks"
handler404 = "tasks.views.custom_404"

urlpatterns = [
    path( 
        "",
        task_home,
        name = "task-home"
    ),
    path(
        "help/",
        TemplateView.as_view(template_name = "tasks/help.html"),
        name = "help"
    ),
    path( 
        "tasks/", # GET
        TaskListView.as_view(),
        name = "task-list"
    ),
    path(
        "tasks/new/", # POST
        TaskCreateView.as_view(),
        name = "task-create"
    ),
    path(
        "tasks/<int:pk>/", # GET 
        TaskDetailView.as_view(),
        name = "task-detail"
    ),
    path(
        "tasks/<int:pk>/edit/", # PUT/PATCH
        TaskUpdateView.as_view(),
        name = "task-update",
    ),
    path(
        "task/<int:pk>/delete/", # DELETE
        TaskDeleteView.as_view(),
        name = "task-delete"
    ),
    path("tasks/<yyyymmdd:date>/",
         task_by_date,
         name = "task-get-by-date"),
    path(
        "task/sprint/add_task/<int:pk>/", # POST
        create_task_on_sprint,
        name = "task-add-to-sprint"
    ),
    path(
        "contact/",
        ContactFormView.as_view(),
        name="contact",
    ),
    path(
        "contact-success/",
        TemplateView.as_view(template_name="contact_success.html"),
        name="contact-success",
    ),
    path(
        "epic/<int:epiic_pk>/",
        manage_epic_tasks,
        name = "task-batch-create"
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
