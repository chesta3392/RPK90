from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from hub import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", views.register, name="register"),
    path("", views.home, name="home"),
    path("play/", views.play, name="play"),
    path("wallet/", views.wallet, name="wallet"),
    path("history/", views.history, name="history"),
    path("results/", views.results, name="results"),
    path("notifications/", views.notifications, name="notifications"),
    path("app-details/", views.app_details, name="app_details"),
    path("terms/", views.terms, name="terms"),
    path("help/", views.help_page, name="help"),
    path("play/demo/<int:game_id>/", views.demo_game, name="demo_game"),
]
