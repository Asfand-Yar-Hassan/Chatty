from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
