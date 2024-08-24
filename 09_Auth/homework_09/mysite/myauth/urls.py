from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    logout_view,
    login_view,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
)

app_name = "myauth"

urlpatterns = [
    path("logout/", MyLogoutView.as_view(), name="logout"),
    # path('login/', login_view, name='login'),
    path(
        "login/",
        LoginView.as_view(
         template_name="myauth/login.html",
         redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
]
