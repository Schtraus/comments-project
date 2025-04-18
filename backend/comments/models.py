from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.username} - {self.text[:30]}"


class FileAttachment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='attachments')  # К какому комментарию относится
    file = models.FileField(upload_to='uploads/')  # Сам файл
    file_type = models.CharField(max_length=10)  # Тип файла (изображение, текст и т.д.)

    def __str__(self):
        return f"Attachment for comment {self.comment.id}"
