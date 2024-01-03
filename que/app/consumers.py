# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage,CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_message(message)

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def save_message(self, message):
        sender = self.scope['user']
        receiver_username = self.scope['url_route']['kwargs']['username']
        receiver = await self.get_user(receiver_username)

        if receiver:
            ChatMessage.objects.create(sender=sender, receiver=receiver, content=message)

    async def get_user(self, username):
        try:
            return await self.channel_layer.group_add(
                f"chat_{username}",
                self.channel_name
            )
        except CustomUser.DoesNotExist:
            return None
