from django.db import models
from account.models import CustomUser  # カスタムユーザーモデルをインポート

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # カスタムユーザーを使用
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

class PostRecipient(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient.username} - {self.post.content[:30]}"
