import json

from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Chat, Message, ChatSettings


class ChatSerializer(serializers.ModelSerializer):
    is_pin = serializers.BooleanField()
    is_mute = serializers.BooleanField()
    is_in_archive = serializers.BooleanField()
    is_last = serializers.BooleanField()
    unread_messages = serializers.IntegerField()
    class Meta:
        model = Chat
        fields = (
            'name',
            'is_group_chat',
            'is_pin',
            'is_mute',
            'is_in_archive',
            'is_last',
            'unread_messages'
        )



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')