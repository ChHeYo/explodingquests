from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.


class TimeStampModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class RewardsModel(models.Model):
    # REWARD_TYPE = (
    #     ('Monetary', 'Monetary'),
    #     ('Non-monetary', 'Non-monetary'),
    # )
    # reward_type = models.CharField(max_length=15, choices=REWARD_TYPE)
    # mon_reward = models.PositiveIntegerField()
    # nonmon_rewards = models.CharField(max_length=255)

#     class Meta:
#         abstract = True


class UserProfile(models.Model):
    username = models.OneToOneField(
                settings.AUTH_USER_MODEL,
                related_name='profile',
                on_delete=models.CASCADE,
               )
    location = models.CharField(max_length=255)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Quest(TimeStampModel):
    REWARD_TYPE = (
        ('Monetary', 'Monetary'),
        ('Non-monetary', 'Non-monetary'),
    )
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='quests',
            on_delete=models.CASCADE
          )
    title = models.CharField(max_length=255)
    description = models.TextField()
    reward_type = models.CharField(max_length=15, choices=REWARD_TYPE, default=REWARD_TYPE[0][0])
    rewards = models.CharField(max_length=255, default='')
    explosion_date = models.DateTimeField()
    # location        = 
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['-date_created']    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quest_detail', kwargs={"slug": self.slug})


def quest_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving...')
    print(instance.date_created)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(quest_pre_save_receiver, sender=Quest)


def get_image_path(instance, filename):
    return '/'.join(['quest_images', instance.quest.slug, filename])


class Upload(models.Model):
    quest = models.ForeignKey(Quest, related_name='uploads')
    image = models.ImageField(upload_to=get_image_path)