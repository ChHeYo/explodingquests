from django import forms

from .models import WorkExperience, Education


class WorkExperienceForm(forms.ModelForm):

    class Meta:
        model = WorkExperience
        exclude = ['user']


class EducationForm(forms.ModelForm): 
    
    class Meta:
        model = Education 
        exclude = ['user']