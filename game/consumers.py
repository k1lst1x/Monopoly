import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class RoomConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.code = self.scope["url_route"]["kwargs"]["code"].upper()
        self.group_name = f"room_{self.code}"
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive_json(self, content):
        if content.get("action") == "roll":
            value = random.randint(1, 6)
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "dice_result", "value": value}
            )

    def dice_result(self, event):
        self.send_json({"type": "dice", "value": event["value"]})
