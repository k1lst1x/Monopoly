from django import forms

from .models import Room


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = []


class JoinRoomForm(forms.Form):
    code = forms.CharField(max_length=6, label="Код комнаты")

    def clean_code(self):
        code = self.cleaned_data["code"].upper()
        if not Room.objects.filter(code=code, is_active=True).exists():
            raise forms.ValidationError("Комната не найдена или закрыта")
        return code
