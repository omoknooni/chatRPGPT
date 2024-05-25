from django.contrib import admin
from .models import Theme, ChatMessage, GameSession

admin.site.register(GameSession)
admin.site.register(Theme)
admin.site.register(ChatMessage)

