from django.urls import path
from . import views
from .views import (
    TaskListView,
    UserTaskListView,
    UnassignedTaskListView,
)

urlpatterns = [
    path("tasks", TaskListView.as_view(), name="tasks"),
    path("task/<int:task_id>", TaskListView.as_view(), name="task"),
    path("mytasks/", UserTaskListView.as_view(), name="user_tasks"),
    path("unassigned/", UnassignedTaskListView.as_view(), name="unassigned_tasks"),
    
    path("", views.login_view, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    path("assign", views.assign, name="assign"),
    path("unassign", views.unassign, name="unassign")
]