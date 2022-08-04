from .models import Message
from asgiref.sync import async_to_sync
from .models import Chat
from common.models import User
from channels.generic.websocket import WebsocketConsumer

import json

class Consumer(WebsocketConsumer):
    def connect(self):
        self.chat_token = self.scope['url_route']['kwargs']['chat_token']
        self.group_name = self.chat_token

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        chat = text_data_json['chat']

        if(chat):
            senderInstance = User.objects.get(pk=sender['pk'])
            chat = Chat.objects.get(pk=chat['pk'])
            newMessage = Message(sender=senderInstance, chat_id=chat, text=message)
            newMessage.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))