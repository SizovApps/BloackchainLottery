from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class AddLotteryForm(forms.ModelForm):
    class Meta:
        model = Lottery
        fields = ['title', 'content', 'gwei_fee', 'max_players', 'photo', 'time_end']
        labels = {
            "title": "Название",
            "content": "Описание",
            "gwei_fee": "Цена билета в Gwei",
            "max_players": "Максимальное количество игроков",
            "photo": "Фотография",
            "time_end": "Время окончания"
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 60, "rows": 10}),
            'time_end': DateInput(),
        }
