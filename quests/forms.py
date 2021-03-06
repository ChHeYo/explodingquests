from datetime import timedelta

from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.utils import timezone

from .models import Quest, Upload, UserProfileImage


class QuestForm(ModelForm):
    
    class Meta:
        model = Quest
        fields = (
            'title',
            'description',
            'reward_type',
            'mon_reward',
            'non_mon_rewards',
            'location',
            'explosion_datetime',
            )
        labels = {
            'reward_type': '',
            "mon_reward": "",
            "non_mon_rewards": "Reward",
            "explosion_datetime": "Detonation Timer",
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    "class": "form-control",
                    'placeholder': "Title",
                     }),
            'description': forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "13",
                    'placeholder': 'Description',
                    }),
            'reward_type': forms.Select(
                attrs={
                    "class": "form-control",
                    }),
            'mon_reward': forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": .01,
                    "placeholder": "Amount: required if monetary",
                    }),
            'non_mon_rewards': forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Reward: required if non-monetary (ie. Free Lunch)",
                }),
            'location': forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Location (optional)",
                }),
            'explosion_datetime': forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "readonly": "readonly",
                }),
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        return super().__init__(*args, **kwargs)

    def clean_explosion_datetime(self):
        exp_datetime = self.cleaned_data.get('explosion_datetime')
        if exp_datetime < timezone.now():
            msg = 'Date cannot be in the past!'
            raise forms.ValidationError(msg)
        elif exp_datetime > timezone.now() + timedelta(days=100):
            msg = "Maximum 100 days in the future"
            raise forms.ValidationError(msg)
        return exp_datetime

    def clean(self):
        cleaned_data = super().clean()
        reward_type = cleaned_data.get('reward_type')
        mon_reward = cleaned_data.get('mon_reward')
        non_mon_rewards = cleaned_data.get('non_mon_rewards')

        if ((reward_type == 'MonetaryH' or reward_type == "MonetaryF")
            and mon_reward is None):
            msg = 'Amount required'
            self.add_error('mon_reward', msg)
        elif ((reward_type == 'MonetaryH' or reward_type == "MonetaryF")
            and mon_reward < 0):
            msg = 'Cannot be negative!'
            self.add_error('mon_reward', msg)

        if ((reward_type == 'MonetaryH' or reward_type == 'MonetaryF')
            and non_mon_rewards is not None):
            msg = 'Please leave this field blank'
            self.add_error('non_mon_rewards', msg)
        
        if (reward_type == 'Non-monetary' and non_mon_rewards is None):
            msg = "Reward required"
            self.add_error('non_mon_rewards', msg)

        if (reward_type == 'Non-monetary' and mon_reward is not None):
            msg = 'Please leave this field blank'
            self.add_error('mon_reward', msg)

        if (reward_type == 'Voluntary' and
        (mon_reward is not None or non_mon_rewards is not None)):
            msg = 'Please leave this field blank'
            self.add_error('mon_reward', msg)
            self.add_error('non_mon_rewards', msg)

        return cleaned_data


class ProfileImageForm(ModelForm):
    class Meta:
        model = UserProfileImage
        fields = ('profile_thumbnail', )
        labels = {
            'profile_thumbnail': "",
        }
        widgets = {
            'profile_thumbnail': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        return super().__init__(*args, **kwargs)


class QuestImageForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('quest_images', )
        labels = {
            'quest_images': "",
        }