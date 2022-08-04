from django.urls import path
from chat import views
urlpatterns = [
    path("chat/", views.ChatListViewSet.as_view()),
    path("chat/create/", views.ChatCreateViewSet.as_view()),
    path("chat/<int:chat_id>/messages/create", views.MessageCreateViewSet.as_view())
]