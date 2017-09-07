import os

from datetime import time, timedelta

from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify


from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from PIL import Image

from .utils import unique_slug_generator
# Create your models here.


def get_image_path(instance, filename):
    # filename, extension = filename.split(".")
    # new_filename = "%s.%s" %(filename+"_thumbnail", extension)
    return '/'.join(['quest_images', instance.quest.slug, filename])


def get_profile_thumbnail_path(instance, filename):
    return '/'.join(['profile_thumbnail', instance.user.username, filename])


class TimeStampModel(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    explosion_datetime = models.DateTimeField(default=timezone.now()+timedelta(days=1))

    class Meta:
        abstract = True


class RewardModel(models.Model):
    REWARD_TYPE = (
        ('MonetaryH', 'Monetary (Hourly)'),
        ('MonetaryF', 'Monetary (Flat)'),
        ('Non-monetary', 'Non-monetary'),
        ('Voluntary', 'Voluntary'),
    )

    MON_REWARD_RATE = (
        ('Hourly', 'Hourly'),
        ('Flat', 'Flat'),
    )

    reward_type = models.CharField(
        max_length=15,
        choices=REWARD_TYPE,
        default=REWARD_TYPE[0][0])
    mon_reward = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,)
    non_mon_rewards = models.CharField(
        max_length=255,
        null=True,
        blank=True,)

    class Meta:
        abstract = True


class UserProfileImage(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile_thumbnail',
        primary_key=True,
        on_delete=models.CASCADE,)
    preferred_name = models.CharField(max_length=200, null=True, blank=True)
    profile_thumbnail = models.ImageField(
        upload_to=get_profile_thumbnail_path,
        null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_thumbnail:
            profile_thumbnail = Image.open(self.profile_thumbnail)
            i_width, i_height = profile_thumbnail.size
            max_size = (200, 200)

            if i_width > 200:
                profile_thumbnail.thumbnail(max_size, Image.ANTIALIAS)
                profile_thumbnail.save(self.profile_thumbnail.path, 'PNG')

    def __str__(self):
        return self.user.username + ' profile_img'

    def image_url(self):
        if self.profile_thumbnail and hasattr(self.profile_thumbnail, 'url'):
            return self.profile_thumbnail.url
        else:
            return '/static/image/default_profile.jpg'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfileImage(user=user)
        profile.save()


class Quest(TimeStampModel, RewardModel):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='quests',
            on_delete=models.CASCADE
          )
    interested_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='interested_users')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    @property
    def past_explosion_date(self):
        if timezone.now() > self.explosion_date:
            return True
        return False

    class Meta:
        ordering = ['-date_created']    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quests:quest_detail', kwargs={"slug": self.slug})


@receiver(pre_save, sender=Quest)
def quest_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving...')
    print(instance.date_created)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Upload(models.Model):
    quest = models.ForeignKey(
        Quest,
        related_name='uploads',
        on_delete=models.CASCADE)
    quest_images = models.ImageField(upload_to=get_image_path)
