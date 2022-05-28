from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatListView.as_view(), name='chat'),
    path('<str:user_id>', views.ChatView.as_view(), name='chat_detail'),
]
