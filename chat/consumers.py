import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import QuerySet
from intra.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            return
        user_id = user.id

        self.room_name = user_id
        self.room_group_name = 'chat_%s' % self.room_name
        username = self.scope['user'].username
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        user = self.scope['user']
        print(user)

    async def send_message_to_chatroom(self, message, username=None):
        data = {
            'body': message,
        }
        if username:
            data['user'] = username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data,
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['user']
        # Send message to room group
        await self.send_message_to_chatroom(message, username)

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
