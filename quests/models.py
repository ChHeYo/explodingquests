from django.db import models
from django.conf import settings

# Create your models here.

class Quest(models.Model):
    DIFFICULTIES = (
        ('E', 'EASY'),
        ('M', 'MEDIUM'),
        ('H', 'HARD'),
    )

    npc             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title           = models.CharField(max_length=255)
    description     = models.CharField(max_length=255)
    objectives      = models.CharField(max_length=255)
    difficulty      = models.CharField(max_length=1, choices=DIFFICULTIES)
    rewards         = models.CharField(max_length=255)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_modified   = models.DateTimeField(auto_now=True)
    explosion_date  = models.DateTimeField()
    slug            = models.SlugField()

    class Meta:
        ordering = ['-date_created']    

    def __str__(self):
        return self.title