from django.urls import path
from .views import chat_with_gpt, chat_history

urlpatterns = [
    path("", chat_with_gpt, name="chat_with_gpt"),
    path("history/", chat_history, name="chat_history"),
]
