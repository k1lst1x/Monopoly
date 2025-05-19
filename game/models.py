import secrets
import string

from django.db import models


def generate_code(k=6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(k))
        if not Room.objects.filter(code=code).exists():
            return code


class Room(models.Model):
    code = models.CharField(
        max_length=6, unique=True, default=generate_code, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Player(models.Model):
    room = models.ForeignKey(Room, related_name="players", on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    order = models.PositiveSmallIntegerField()
    money = models.IntegerField(default=1500)
    position = models.PositiveSmallIntegerField(default=0)
    is_turn = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("room", "order")

    def __str__(self):
        return f"{self.nickname} ({self.room.code})"
