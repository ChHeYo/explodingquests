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
    sender              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver            = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')
    related_quest       = models.ForeignKey(Quest, related_name='related_quest')
    parent              = models.ForeignKey('self', related_name='replies', blank=True, null=True)
    subject             = models.CharField(max_length=250)
    content             = models.TextField()
    trash_by_sender     = models.BooleanField(default=False)
    trash_by_receiver   = models.BooleanField(default=False)
    viewed_by_receiver  = models.BooleanField(default=False)
    send_at             = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('dashboard:message_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.subject + ': ' + self.content[:10]

    def read_by_receiver(self):
        if not self.viewed_by_receiver:
            self.viewed_by_receiver = True
            self.save()

    class Meta:
        ordering = ['send_at']


class ContactUs(models.Model):
    contact_info    = models.CharField(max_length=250)
    content         = models.TextField()

    def __str__(self):
        return self.contact_info