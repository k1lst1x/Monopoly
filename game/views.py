from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from .forms import CreateRoomForm, JoinRoomForm
from .models import Room


def generate_board_cells(size=10):
    coords = []
    for col in reversed(range(size + 1)):
        coords.append((size, col))
    for row in reversed(range(size)):
        coords.append((row, 0))
    for col in range(1, size + 1):
        coords.append((0, col))
    for row in range(1, size):
        coords.append((row, size))

    return [{"i": idx, "row": r + 1, "col": c + 1} for idx, (r, c) in enumerate(coords)]


class BoardView(TemplateView):
    template_name = "game/board.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        size = 10  # внешний периметр 10×10 => сетка 11×11
        coords = []

        # 1) нижний ряд (справа-налево)
        for col in reversed(range(size + 1)):
            coords.append((size, col))
        # 2) левый столбец (снизу-вверх, кроме угла)
        for row in reversed(range(size)):
            coords.append((row, 0))
        # 3) верхний ряд (слева-направо, кроме угла)
        for col in range(1, size + 1):
            coords.append((0, col))
        # 4) правый столбец (сверху-вниз, кроме угла)
        for row in range(1, size):
            coords.append((row, size))

        ctx["cells"] = [
            {"i": idx, "row": r + 1, "col": c + 1}  # +1 — grid счёт с 1
            for idx, (r, c) in enumerate(coords)
        ]
        return ctx


class CreateRoomView(FormView):
    template_name = "game/create.html"
    form_class = CreateRoomForm

    def form_valid(self, form):
        room = form.save()
        return RedirectView.as_view(
            url=reverse_lazy("game:room", kwargs={"code": room.code})
        )(self.request)


class JoinRoomView(FormView):
    template_name = "game/join.html"
    form_class = JoinRoomForm

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        return RedirectView.as_view(
            url=reverse_lazy("game:room", kwargs={"code": code})
        )(self.request)


class BoardRoomView(TemplateView):
    template_name = "game/room.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["room_code"] = self.kwargs["code"].upper()
        ctx["cells"] = generate_board_cells()
        return ctx
