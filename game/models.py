from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    theme = models.CharField(max_length=100)
    players = models.ManyToManyField(User, related_name='game_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    chat_channel_id = models.CharField(max_length=100, unique=True, null=True, blank=True)


class ChatMessage(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:20]}..."

class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name