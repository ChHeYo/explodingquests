from datetime import datetime, date, time

from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.utils import timezone

from .models import Quest


class QuestForm(ModelForm):
    
    class Meta:
        model = Quest
        fields = (
            'title',
            'description',
            'reward_type',
            'mon_reward_rate',
            'mon_reward',
            'non_mon_rewards',
            'explosion_datetime',
            )
        labels = {
            "mon_reward_rate": "Rate",
            "mon_reward": "Amount",
            "non_mon_rewards": "Reward",
            "explosion_datetime": "Detonation Timer (default = +1 day)",
        }
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", }),
            'description': forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "10",
                    }),
            'reward_type': forms.Select(attrs={"class": "form-control", }),
            'mon_reward_rate': forms.Select(attrs={"class": "form-control", }),
            'mon_reward': forms.NumberInput(
                attrs={
                    "class": "form-control", 
                    "step": .01, 
                    "placeholder": "Non-negative number with 2 decimal places"
                    }),
            'non_mon_rewards': forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "i.e. Free Lunch",
                }),
            'explosion_datetime': forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                }),
        }

    def clean_explosion_datetime(self):
        exp_datetime = self.cleaned_data.get('explosion_datetime')

        if exp_datetime < timezone.now():
            raise forms.ValidationError("Date cannot be in the past!")

        return exp_datetime

    def clean_mon_reward(self):
        if self.cleaned_data.get('mon_reward'):
            mon_rewd = self.cleaned_data.get('mon_reward')

            if mon_rewd < 0:
                raise forms.ValidationError("Cannot be negative!")
            return mon_rewd


    # def print_explosion_date(self):
    #     exp_date = self.clean_explosion_data.get('explosion_date')
    #     print(exp_date)
    #     returned example => 2017-08-07T22%3A20