from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from .utils import unique_slug_generator
from django.db.models.signals import pre_save

# Create your models here.

class TimeStampModel(models.Model):
    date_created    = models.DateTimeField(auto_now_add=True)
    date_modified   = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Quest(TimeStampModel):

    npc             = models.ForeignKey(
                        settings.AUTH_USER_MODEL,
                        related_name='quests',
                        on_delete=models.CASCADE
                      )
    title           = models.CharField(max_length=255)
    description     = models.TextField()
    rewards         = models.CharField(max_length=255)
    explosion_date  = models.DateTimeField()
    # category        =
    # location        = 
    slug            = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['-date_created']    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quest_detail', kwargs={"slug":self.slug})

def quest_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving...')
    print(instance.date_created)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(quest_pre_save_receiver, sender=Quest)
