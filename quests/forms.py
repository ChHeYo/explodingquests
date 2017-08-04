from django import forms
from django.forms import ModelForm
from django.utils import timezone

from .models import Quest


class QuestForm(ModelForm):
    class Meta:
        model = Quest
        fields = ('title', 'description', 'reward_type', 'rewards', 'explosion_date')
        widgets = {
            'explosion_date': forms.DateTimeInput(attrs={"type": "date"})
        }

    def clean_explosion_date(self):
        ex_date = self.cleaned_data.get('explosion_date') 

        if ex_date < timezone.now(): 
            raise forms.ValidationError("The date cannot be in the past!")
        return ex_date