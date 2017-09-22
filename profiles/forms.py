from django import forms

from .models import (
    WorkExperience, Education,
    DefuseMessage, ContactUs)


class WorkExperienceForm(forms.ModelForm):

    class Meta:
        model = WorkExperience
        fields = (
            'company',
            'title',
            'description',
            'started_date',
            'end_date',
        )
        widgets = {
            'title': forms.TextInput(
                attrs={
                    "class": "form-control",
                    'placeholder': "Title",
                     }),
            'company': forms.TextInput(
                attrs={
                    "class": "form-control",
                    'placeholder': "Company",
                     }),
            'description': forms.Textarea(
                attrs={
                    "class": "form-control",
                    'placeholder': "Description",
                     }),
            'started_date': forms.DateInput(
                attrs={
                    "class": "form-control",
                    'placeholder': "From",
                    "readonly": "readonly",
                     }),
            'end_date': forms.DateInput(
                attrs={
                    "class": "form-control",
                    'placeholder': "To",
                    "readonly": "readonly",
                     }),
        }


class EducationForm(forms.ModelForm): 
    
    class Meta:
        model = Education 
        exclude = ['user']


class SendMessageForm(forms.ModelForm):

    class Meta:
        model = DefuseMessage
        fields = (
            'subject',
            'content',
        )
        labels = {
            'subject': '',
            'content': '',
        }
        widgets = {
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Subject',
                }),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Content',
                }),
        }


class ReplyForm(forms.ModelForm):

    class Meta:
        model = DefuseMessage
        fields = (
            'content',
        )
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 6,
                    'onfocus':"this.placeholder = ''",
                    'placeholder': 'Click here to reply',
                }),
        }


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = (
            'contact_info',
            'content',
        )
        widgets = {
            'contact_info': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Best way to reach you',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'What do you need help with?',
                }
            ),
        }