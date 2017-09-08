from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from quests.models import Quest

# Create your models here.

class Duration(models.Model):
    started_date = models.DateField()
    end_date     = models.DateField()

    class Meta:
        abstract = True

class WorkExperience(Duration):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='work_experience')
    title       = models.CharField(max_length=250, blank=True, null=True)
    company     = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('dashboard:my_profile')

    def __str__(self):
        return self.title


class Education(Duration):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='education') 
    school      = models.CharField(max_length=250, null=True, blank=True)
    degree      = models.CharField(max_length=250, null=True, blank=True)
    major       = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.school


class DefuseMessage(models.Model):
    sender          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver        = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')
    related_quest   = models.ForeignKey(Quest, related_name='related_quest')
    subject         = models.CharField(max_length=250)
    content         = models.TextField()
    send_at         = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('profiles:message_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.sender.username
    
