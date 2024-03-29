from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from Portfolio.models import Profile, Job


@receiver(post_save, sender=User)
def on_user_register(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
