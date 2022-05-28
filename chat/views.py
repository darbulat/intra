from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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
