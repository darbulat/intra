import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import QuerySet, Q

from chat.models import MessageModel
from intra.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

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
        recipient_id = text_data_json['recipient_id']
        await self.save_message(body=message, recipient_id=recipient_id, username=username)
        # Send message to room group
        await self.send_message_to_chatroom(message, username)

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, body: str, recipient_id: int, username: str):
        user = User.objects.get(username=username)
        MessageModel.objects.create(user=user, recipient_id=recipient_id, body=body)
