from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("plan", views.plan_view, name="plan"),
    path("homework", views.homework_view, name="homework"),
    path("submission/<int:homework_id>", views.homework_submission_view, name="submission")
]