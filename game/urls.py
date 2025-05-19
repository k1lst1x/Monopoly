from django.urls import path

from . import views

app_name = "game"

urlpatterns = [
    path("board/", views.BoardView.as_view(), name="board"),  # статичное демо
    path("create/", views.CreateRoomView.as_view(), name="create"),
    path("join/", views.JoinRoomView.as_view(), name="join"),
    path("<str:code>/", views.BoardRoomView.as_view(), name="room"),
]
