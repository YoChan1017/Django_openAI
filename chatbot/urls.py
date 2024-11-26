from django.urls import path
from .views import create_chatbot, chatbot_log
from .chatbot_chat import chatbot_chat

urlpatterns = [
    path('', create_chatbot, name='create_chatbot'),
    path('chat/', chatbot_chat, name='chatbot_chat'),
    path('log/', chatbot_log, name='chatbot_log'),
]
