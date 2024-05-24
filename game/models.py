from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    theme = models.CharField(max_length=100)
    players = models.ManyToManyField(User, related_name='game_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name