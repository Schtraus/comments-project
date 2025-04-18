from django.shortcuts import render

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
    ordering_fields = ['username', 'email', 'created_at']  # 👈 Разрешённые поля
    ordering = ['-created_at']


@api_view(['GET'])
def get_captcha(request):
    new_captcha = CaptchaStore.generate_key()
    image_url = captcha_image_url(new_captcha)
    return Response({
        'key': new_captcha,
        'image_url': image_url
    })