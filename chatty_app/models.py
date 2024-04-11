from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="chatrooms")
    user_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_user_count(self):
        self.user_count = self.users.count()
        self.save()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
