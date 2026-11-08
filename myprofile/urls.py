from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_view, name="home"),
    path("task/", views.tasks_view, name="tasks"),
    path("/settings/", views.settings_view, name="settings"),
]