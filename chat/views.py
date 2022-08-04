from django.db.models import Count
from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from django.db import models
from rest_framework.permissions import IsAuthenticated

from chat.models import Chat, Message, ChatSettings
from chat.serializer import ChatSerializer, MessageSerializer
from common.models import User
from chat import serializer


class ChatCreateViewSet(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class ChatListViewSet(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(members=self.request.user).annotate(
            is_pin=ChatSettings.objects.filter(chat_id=models.OuterRef('id'), user=self.request.user).values('is_pin'),
            is_mute=ChatSettings.objects.filter(chat_id=models.OuterRef('id'), user=self.request.user).values('is_mute'),
            is_in_archive=ChatSettings.objects.filter(chat_id=models.OuterRef('id'), user=self.request.user).values('is_in_archive'),
            is_last=ChatSettings.objects.filter(chat_id=models.OuterRef('id'), user=self.request.user).values('is_last'),
        )
        return queryset


class MessageCreateViewSet(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]