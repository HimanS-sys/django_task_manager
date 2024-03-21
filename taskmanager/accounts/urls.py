
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views
app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        views.register,
        name="register"
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name = "accounts/login.html"
        ),
        name = "login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name = "logout",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            success_url = reverse_lazy("accounts:password_change_done"),
            template_name = "accounts/password_change_form.html",
        ),
        name = "password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
        template_name = "accounts/password_change_done.html"
        ),
        name = "password_change_done",
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            email_template_name = "accounts/custom_password_reset_email.html",
        ),
        name = "password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name = "password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name = "password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name = "password_reset_complete",
    ),
]
