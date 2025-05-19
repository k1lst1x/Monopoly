import json
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.utils.crypto import get_random_string

from .models import Player, Room


class RoomConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.code = self.scope["url_route"]["kwargs"]["code"].upper()
        self.room = Room.objects.get(code=self.code)
        self.group_name = f"room_{self.code}"
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def receive_json(self, content):
        act = content.get("action")
        if act == "join":
            nick = content.get("nickname") or f"Player-{get_random_string(4)}"
            order = self.room.players.count() + 1
            is_first = order == 1
            player = Player.objects.create(
                room=self.room, nickname=nick, order=order, is_turn=is_first
            )
            self.send_state()
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "broadcast_state"}
            )
        elif act == "roll":
            self.handle_roll()

    def handle_roll(self):
        player = self.room.players.get(is_turn=True)
        value = random.randint(1, 6)
        player.position = (player.position + value) % 40
        player.is_turn = False
        player.save()

        next_order = (player.order % self.room.players.count()) + 1
        next_player = self.room.players.get(order=next_order)
        next_player.is_turn = True
        next_player.save()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "dice_result", "value": value}
        )
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "broadcast_state"}
        )

    def dice_result(self, event):
        self.send_json({"type": "dice", "value": event["value"]})

    def broadcast_state(self, event):
        self.send_state()

    def send_state(self):
        players = list(
            self.room.players.order_by("order").values(
                "order", "nickname", "money", "position", "is_turn"
            )
        )
        self.send_json({"type": "state", "players": players})
