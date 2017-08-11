from PIL import Image

from datetime import time, timedelta

from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify

from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.


def get_image_path(instance, filename):
    return '/'.join(['quest_images', instance.quest.slug, filename])


def get_profile_image_path(instance, filename):
    return '/'.join(['profile_images', instance.username.username, filename])


class TimeStampModel(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    explosion_datetime = models.DateTimeField(default=timezone.now()+timedelta(days=1))

    class Meta:
        abstract = True


class RewardModel(models.Model):
    REWARD_TYPE = (
        ('Monetary', 'Monetary'),
        ('Non-monetary', 'Non-monetary'),
    )

    MON_REWARD_RATE = (
        ('Hourly', 'Hourly'),
        ('Flat', 'Flat'),
    )

    reward_type = models.CharField(
        max_length=15, 
        choices=REWARD_TYPE, 
        default=REWARD_TYPE[0][0])
    mon_reward_rate = models.CharField(
        max_length=10, 
        choices=MON_REWARD_RATE,
        default=MON_REWARD_RATE[0][0],
        null=True,
        blank=True,)
    mon_reward = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,)
    non_mon_rewards = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        primary_key=True,
        on_delete=models.CASCADE,)
    location = models.CharField(max_length=255)
    profile_image = models.ImageField(
        upload_to=get_profile_image_path,
        null=True,)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        if self.profile_image:
            image = Image.open(self.profile_image)
            i_width, i_height = image.size
            max_size = (200, 200)

            if i_width > 200:
                image.thumbnail(max_size, Image.ANTIALIAS)
                image.save(self.profile_image.path)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()


class Quest(TimeStampModel, RewardModel):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='quests',
            on_delete=models.CASCADE
          )
    title = models.CharField(max_length=255)
    description = models.TextField()
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
        return reverse('quest_detail', kwargs={"slug": self.slug})


@receiver(pre_save, sender=Quest)
def quest_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving...')
    print(instance.date_created)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Upload(models.Model):
    quest = models.ForeignKey(Quest, related_name='uploads')
    image = models.ImageField(upload_to=get_image_path)
