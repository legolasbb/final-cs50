from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("plan", views.plan_view, name="plan"),
    path("te_homework", views.homework_teacher_view, name="te_homework"),
]