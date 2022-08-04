from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from django.conf import settings
from django.contrib.auth.models import AbstractUser
import json
from django.db import models
# from django.utils import timezone
from common.models import User
from helpers.models import BaseModel


class Chat(BaseModel):
    name = models.CharField(max_length=255, null=True)
    chat_token = models.CharField(max_length=255)
    is_group_chat = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='users')


TEXT = "text"
AUDIO = "audio"
VIDEO = "video"
FILE = "file"
MESSAGE_TYPE = (
    (TEXT, "text"),
    (AUDIO, "audio"),
    (VIDEO, "video"),
    (FILE, "file"),
)


class Message(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=MESSAGE_TYPE)
    text = models.TextField(null=True)
    is_view = models.BooleanField(default=False)


@receiver(post_save, sender=Message)
def message_handler(sender, instance, created, **kwargs):
    chat_token = instance.chat.chat_token
    channel_layer = get_channel_layer()
    if created:
        async_to_sync(channel_layer.group_send)(
            chat_token, {"type": "chat_message", "data": {
                "id": instance.id,
                "status": "new_message",
                "text": instance.text,
                "chat_id": instance.chat_id,
                "from_user_id": instance.sender_id,
            }}
        )
    else:
        async_to_sync(channel_layer.group_send)(
            chat_token, {"type": "chat_message", "data": {
                "id": instance.id,
                "status": "updated_message",
                "text": instance.text,
                "chat_id": instance.chat_id,
                "from_user_id": instance.sender_id,
            }}
        )


class ChatSettings(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_settings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pin = models.BooleanField(default=False)
    is_last = models.BooleanField(default=True)
    is_mute = models.BooleanField(default=False)
    is_in_archive = models.BooleanField(default=False)