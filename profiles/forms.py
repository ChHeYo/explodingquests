from django import forms

from .models import WorkExperience, Education


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