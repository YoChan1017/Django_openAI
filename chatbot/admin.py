from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'location', 'days', 'created_at')
    search_fields = ('session_id', 'location')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'user_message', 'bot_response', 'timestamp')
    search_fields = ('session__session_id', 'user_message', 'bot_response')
