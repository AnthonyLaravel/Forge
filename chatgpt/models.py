# chatgpt/models.py
from django.db import models
from django.contrib.auth.models import User


class ChatRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_requests')
    prompt = models.TextField()
    response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request by {self.user.username} on {self.created_at}"
