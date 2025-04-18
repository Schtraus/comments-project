from django.contrib import admin
from .models import Comment, FileAttachment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at', 'parent')  # поля, которые видны в списке
    list_filter = ('created_at',)
    search_fields = ('username', 'email', 'text')
    readonly_fields = ('created_at',)


@admin.register(FileAttachment)
class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'file', 'file_type')
    list_filter = ('file_type',)
