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
            'explosion_date')
        labels = {
            "mon_reward_rate": "Rate",
            "mon_reward": "Amount",
            "non_mon_rewards": "Reward",
            "explosion_date": "Detonation Date",
        }
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", }),
            'description': forms.Textarea(attrs={"class": "form-control", }),
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
            'explosion_date': forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "MM/DD/YYYY",
                }),
        }

    def clean_explosion_date(self):
        ex_date = self.cleaned_data.get('explosion_date') 

        if ex_date < timezone.now(): 
            raise forms.ValidationError("The date cannot be in the past!")
        return ex_date

    def clean_mon_reward(self):
        mon_rewd = self.cleaned_data.get('mon_reward')

        if mon_rewd < 0:
            raise forms.ValidationError("Cannot be negative!")
        return mon_rewd

    # def print_explosion_date(self):
    #     exp_date = self.clean_explosion_data.get('explosion_date')
    #     print(exp_date)
    #     returned example => 2017-08-07T22%3A20