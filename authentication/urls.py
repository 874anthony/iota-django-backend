from django.urls import path
from .views import login_github, github_callback

urlpatterns = [
    path("login/", login_github, name="login_github"),
    path("callback/", github_callback, name="github_callback"),
]
