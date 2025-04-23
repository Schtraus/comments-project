from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rest_framework import generics, filters
from .models import Comment
from .serializers import CommentSerializer
from .pagination import CommentPagination

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None).order_by('-created_at')
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        comment = serializer.save()

        # WebSocket пуш
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "comments",
            {
                "type": "send_new_comment",
                "data": CommentSerializer(comment).data
            }
        )


@api_view(['GET'])
def get_captcha(request):
    new_captcha = CaptchaStore.generate_key()
    image_url = captcha_image_url(new_captcha)
    return Response({
        'key': new_captcha,
        'image_url': image_url
    })