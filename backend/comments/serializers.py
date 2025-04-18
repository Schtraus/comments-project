import os
from rest_framework import serializers
from .models import Comment, FileAttachment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from PIL import Image
import bleach


ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title']
}


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = ['id', 'file', 'file_type']


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        # value — это объект комментария (дочерний)
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    attachments = FileAttachmentSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    replies = RecursiveField(many=True, read_only=True)

    captcha_key = serializers.CharField(write_only=True)
    captcha_text = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'username', 'email', 'homepage', 'text', 'created_at',
            'parent', 'attachments', 'replies', 'uploaded_files',
            'captcha_key', 'captcha_text'
        ]

    def validate_text(self, value):
        cleaned = bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        return cleaned

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        comment = Comment.objects.create(**validated_data)

        for f in uploaded_files:
            ext = os.path.splitext(f.name)[1].lower()
            file_type = 'image' if ext in ['.jpg', '.jpeg', '.png', '.gif'] else 'text'

            if file_type == 'text' and ext != '.txt':
                raise ValidationError("Допускается только .txt для текстовых файлов.")
            if f.size > 100 * 1024:
                raise ValidationError("Файл слишком большой (макс. 100KB)")

            attachment = FileAttachment.objects.create(comment=comment, file=f, file_type=file_type)

            if file_type == 'image':
                self._resize_image(attachment.file.path)

        return comment

    def _resize_image(self, file_path):
        with Image.open(file_path) as img:
            if img.width > 320 or img.height > 240:
                img.thumbnail((320, 240))
                img.save(file_path)
    
    def validate(self, data):
        # Валидация капчи
        from captcha.models import CaptchaStore
        key = data.pop('captcha_key', None)
        user_input = data.pop('captcha_text', '').strip().lower()

        try:
            captcha = CaptchaStore.objects.get(hashkey=key)
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError({"captcha": "Неверный ключ капчи."})

        if captcha.response != user_input:
            raise serializers.ValidationError({"captcha": "Неверный текст капчи."})

        captcha.delete()  # удалим, чтобы нельзя было переиспользовать

        return data


