from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    ebay_authorization_code = models.CharField(max_length=255, blank=True, null=True)
    ebay_authorization_code_expires_in = models.IntegerField(blank=True, null=True)
    ebay_access_token = models.TextField(null=True, blank=True)
    ebay_token_expires_in = models.DateTimeField(blank=True, null=True)
    ebay_refresh_token = models.TextField(null=True, blank=True)
    ebay_refresh_token_expires_in = models.DateTimeField(blank=True, null=True)
    ebay_token_type = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_member(sender, instance, **kwargs):
    instance.member.save()
