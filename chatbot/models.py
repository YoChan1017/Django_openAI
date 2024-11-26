from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """10분 이상 지난 세션인지 확인"""
        expiration_time = self.created_at + timedelta(minutes=10)
        return now() > expiration_time

    def __str__(self):
        return f"Session {self.session_id} for {self.location} ({self.days} days)"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message in Session {self.session.session_id} at {self.timestamp}"
