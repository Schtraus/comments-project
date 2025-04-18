from django.urls import path
from .views import CommentListCreateView, get_captcha

urlpatterns = [
    path('comments/', CommentListCreateView.as_view(), name='comments-list-create'),
    path('captcha/', get_captcha),
]
