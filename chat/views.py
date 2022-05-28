from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from .models import MessageModel
from intra.models import User


class ChatListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = MessageModel.objects.filter()
    template_name = 'chat/chat_list.html'
    paginate_by = 10

    def get_queryset(self):
        all_messages = self.queryset.filter(
            Q(recipient=self.request.user) |
            Q(user=self.request.user)
        ).order_by('-date')
        messages_ok = []
        partners = list()
        for message in all_messages:
            key = {message.user.id, message.recipient.id}
            if key in partners:
                continue
            messages_ok.append(message.id)
            partners.append(key)
        return all_messages.filter(pk__in=messages_ok)


class ChatView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'chat/room.html'

    def get(self, request, user_id):
        recipient = User.objects.get(pk=user_id)
        author = self.request.user
        messages = MessageModel.objects.filter(
            Q(recipient=recipient, user=author) | Q(user_id=recipient, recipient_id=author)
        ).select_related('user').order_by('date')
        return render(
            request,
            self.template_name,
            {
                'user_id': user_id,
                'recipient_username': recipient.username,
                'recipient_last_name': recipient.last_name,
                'recipient_first_name': recipient.first_name,
                'message_list': list(messages),
            }
        )

    def get_all_messages(self, author_id: int, recipient_id: int):
        messages = MessageModel.objects.filter(
            Q(recipient_id=recipient_id, user_id=author_id) | Q(user_id=recipient_id, recipient_id=author_id)
        ).select_related('user').order_by('date')
        return list(messages)
